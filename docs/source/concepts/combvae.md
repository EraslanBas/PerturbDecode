# The ComBVAE model

:::{admonition} Draft
:class: caution
Architecture below is accurate to the implementation; the interpretation
sections need writing.
:::

ComBVAE is a conditional variational autoencoder over single-cell expression,
conditioned on perturbation identity.

## Why this model

<!-- TODO: write this section. Points to cover:
     - Why single-gene perturbation effects are hard to detect: signal is sparse
       and subtle.
     - Why the whole perturbation space is modelled jointly rather than one
       perturbation at a time.
     - What the beta weighting buys: disentangled program embeddings, and why
       that makes small shifts detectable.
     - Why measuring shifts at the embedding level beats measuring them per
       gene, given correlation structure across genes (the unequal-pathway-size
       problem).
     - Why a non-linear model is needed at all.
-->

## Architecture

```text
        perturbation one-hot (n_cond_in)
                    |
            EmbeddingLayer  ->  c  (n_cond)
                    |
   x ---------------+----------------> Encoder -> means, log_var  (n_latents)
                                            |
                                    reparameterise -> z
                                            |
   c ---------------------------------------+----> Decoder -> recon_x
```

- **Encoder**: `Linear(n_inputs + n_cond, 512)` → `BatchNorm1d` → `ReLU` →
  `Linear(512, 512)`, then two heads producing the latent mean and log-variance.
- **Decoder**: `Linear(n_latents + n_cond, 512)` → `ReLU` →
  `Linear(512, n_inputs)`.
- **Embedding**: a linear map from the one-hot perturbation vector to a dense
  `n_cond`-dimensional representation. This is the object of interest: the
  learned perturbation embedding.

## Loss

$$
\mathcal{L} = \frac{1}{N}\Big( \underbrace{\lVert \hat{x} - x \rVert^2}_{\text{reconstruction}} + \alpha \underbrace{D_{\mathrm{KL}}\big(q(z \mid x, c) \,\Vert\, \mathcal{N}(0, I)\big)}_{\text{regularisation}} \Big)
$$

Reconstruction is summed squared error; $\alpha$ weights the KL term.

:::{note}
An L1 penalty on the perturbation embedding appears in earlier versions of this
code but was never included in the optimised total, so it did not influence
training. The packaged model omits it. See the release notes.
:::

## The Gumbel variant

`CVAE_Gumbel` replaces the plain embedding with a Gumbel-sigmoid relaxation,
which encourages a sparse, approximately binary mask over embedding dimensions.
The temperature `tau` controls how hard the relaxation is.

<!-- TODO: when to prefer the Gumbel variant; how to choose tau; what the mask
     means biologically. -->

## Interpreting the embedding

<!-- TODO: what distances in embedding space mean, how to cluster it, and the
     relationship between the embedding and the beta matrix from stage 04. -->

## Choosing hyperparameters

<!-- TODO: n_latents, n_cond, alpha, learning rate, epochs -- with the
     reasoning, not just the defaults. -->
