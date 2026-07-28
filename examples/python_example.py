# Python example
"""Minimal example of using PerturbDecode from Python.

Builds a small synthetic screen, instantiates the conditional VAE and runs a
single forward pass. Requires no real data, so it doubles as a smoke test of
the installation::

    python examples/python_example.py
"""

# NOTE: import perturbdecode before torch. On conda installs whose system
# libstdc++ predates GLIBCXX_3.4.26, importing torch first makes the later
# scanpy/numba import fail with "Could not load shared object file:
# libllvmlite.so". Putting conda's lib directory on LD_LIBRARY_PATH fixes it
# permanently and makes the order irrelevant.
from perturbdecode.models import CVAE_basic, CVAE_basic_get_loss_fn
from perturbdecode.utils import numpy_to_tensor

import numpy as np
import torch


def main():
    n_cells, n_genes, n_perturbations = 64, 50, 4
    n_latents, n_cond = 8, 5

    # A random expression matrix and one-hot perturbation labels.
    expression = np.random.randn(n_cells, n_genes).astype("float32")
    perturbations = np.eye(n_perturbations, dtype="float32")[
        np.random.randint(0, n_perturbations, n_cells)
    ]

    x = numpy_to_tensor(expression)
    c = numpy_to_tensor(perturbations)

    model = CVAE_basic(
        n_inputs=n_genes,
        n_latents=n_latents,
        n_cond=n_cond,
        n_cond_in=n_perturbations,
    )

    recon_x, _, means, log_var, c_emb = model(x, c)
    loss, mse, kld = CVAE_basic_get_loss_fn(alpha=1.0)(
        recon_x, x, means, log_var, c_emb
    )

    print(f"reconstruction shape   : {tuple(recon_x.shape)}")
    print(f"latent means shape     : {tuple(means.shape)}")
    print(f"perturbation embedding : {tuple(c_emb.shape)}")
    print(f"loss={loss.item():.3f}  mse={mse.item():.3f}  kl={kld.item():.3f}")

    # Latent representation for downstream analysis.
    with torch.no_grad():
        latent = model.inference(x, c)
    print(f"latent representation  : {tuple(latent.shape)}")


if __name__ == "__main__":
    main()
