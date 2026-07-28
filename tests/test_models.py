"""Tests for the ComBVAE model implementations."""

import pytest

torch = pytest.importorskip("torch")

from perturbdecode.models import (  # noqa: E402
    CVAE_basic,
    CVAE_basic_get_loss_fn,
    CVAE_Gumbel,
    CVAE_Gumbel_get_loss_fn,
)

N_INPUTS, N_LATENTS, N_COND, N_COND_IN, BATCH = 40, 8, 5, 3, 16


def make_basic():
    """Construct a CVAE_basic with the test dimensions."""
    return CVAE_basic(
        n_inputs=N_INPUTS, n_latents=N_LATENTS, n_cond=N_COND, n_cond_in=N_COND_IN
    )


def make_gumbel():
    """Construct a CVAE_Gumbel with the test dimensions."""
    return CVAE_Gumbel(
        n_inputs=N_INPUTS,
        n_latents=N_LATENTS,
        n_cond=N_COND,
        n_cond_in=N_COND_IN,
        tau=2.0,
    )


MODEL_FACTORIES = [pytest.param(make_basic, id="basic"), pytest.param(make_gumbel, id="gumbel")]


def _batch():
    return torch.randn(BATCH, N_INPUTS), torch.randn(BATCH, N_COND_IN)


@pytest.mark.parametrize("factory", MODEL_FACTORIES)
def test_forward_shapes(factory):
    """Forward pass returns correctly shaped reconstruction and latent stats."""
    net = factory()
    x, c = _batch()
    recon_x, x_out, means, log_var, c_emb = net(x, c)

    assert recon_x.shape == (BATCH, N_INPUTS)
    assert x_out.shape == (BATCH, N_INPUTS)
    assert means.shape == (BATCH, N_LATENTS)
    assert log_var.shape == (BATCH, N_LATENTS)
    assert c_emb.shape == (BATCH, N_COND)


@pytest.mark.parametrize("factory", MODEL_FACTORIES)
def test_inference_and_generate(factory):
    """``inference`` returns latent means; ``generate`` reconstructs from z."""
    net = factory()
    x, c = _batch()

    assert net.inference(x, c).shape == (BATCH, N_LATENTS)
    assert net.generate(torch.randn(BATCH, N_LATENTS), c).shape == (BATCH, N_INPUTS)


@pytest.mark.parametrize("factory", MODEL_FACTORIES)
def test_embedding_shape(factory):
    """The perturbation embedding maps n_cond_in -> n_cond."""
    net = factory()
    _, c = _batch()
    assert net.get_embedding(c).shape == (BATCH, N_COND)


@pytest.mark.parametrize(
    "factory, loss_factory",
    [
        pytest.param(make_basic, CVAE_basic_get_loss_fn, id="basic"),
        pytest.param(make_gumbel, CVAE_Gumbel_get_loss_fn, id="gumbel"),
    ],
)
def test_loss_is_finite_scalar(factory, loss_factory):
    """Loss is a finite scalar; its components are non-negative."""
    net = factory()
    x, c = _batch()
    loss, bce, kld = loss_factory(1.0)(*net(x, c))

    assert loss.ndim == 0
    assert torch.isfinite(loss)
    assert bce.item() >= 0
    assert kld.item() >= -1e-6  # KL against a standard normal


def test_kl_weight_changes_loss():
    """The KL weight actually influences the total loss."""
    net = make_basic()
    net.eval()  # freeze BatchNorm so both losses see identical statistics
    x, c = _batch()
    with torch.no_grad():
        out = net(x, c)

    low = CVAE_basic_get_loss_fn(0.0)(*out)[0]
    high = CVAE_basic_get_loss_fn(10.0)(*out)[0]

    assert not torch.isclose(low, high), "KL weight had no effect on the loss"


def test_backward_pass_produces_gradients():
    """A backward pass propagates non-zero gradients to model parameters."""
    net = make_basic()
    loss, _, _ = CVAE_basic_get_loss_fn(1.0)(*net(*_batch()))
    loss.backward()

    grads = [p.grad for p in net.parameters() if p.requires_grad]
    assert grads, "model reported no trainable parameters"
    assert any(g is not None and torch.any(g != 0) for g in grads)


def test_embedding_is_trainable():
    """Gradients reach the perturbation embedding layer specifically."""
    net = make_basic()
    loss, _, _ = CVAE_basic_get_loss_fn(1.0)(*net(*_batch()))
    loss.backward()

    emb_grads = [p.grad for p in net.embedding.parameters()]
    assert any(g is not None and torch.any(g != 0) for g in emb_grads)
