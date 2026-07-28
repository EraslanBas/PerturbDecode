PerturbDecode
=============

An end-to-end toolkit for analysing large-scale single-cell perturbation
screens: from guide-level quality control through perturbation effect sizes to
generative modelling of perturbation responses with ComBVAE.

Installation
------------

.. code-block:: bash

   pip install PerturbDecode           # core
   pip install 'PerturbDecode[r]'      # with the optional R integration

The core install has no R dependency. Steps that call into R raise a clear
error telling you to install the ``[r]`` extra.

Quickstart
----------

.. code-block:: python

   import perturbdecode as pd

   # Split a screen into training and validation sets
   pd.createTrainValData(
       adata,
       perturbationColumn="perturbation",
       pertCategories=["control", "KO_A", "KO_B"],
       dataDir="out/",
   )

   # Train the conditional VAE
   pd.runTrainingComBVAE(model_dir="out/models", ...)

   # Pull out the learned perturbation embeddings
   emb = pd.extract_model_embeddings(model_dir="out/models", ...)

List the available steps from the command line:

.. code-block:: bash

   perturbdecode list-steps

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
