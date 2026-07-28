API Reference
=============

Pipeline steps
--------------

The functions below are the pipeline entry points and are re-exported at the
package root, so ``perturbdecode.createTrainValData`` and
``perturbdecode.pertdec.createTrainValData`` are the same object.

.. automodule:: perturbdecode.pertdec.createTrainValData
   :members:

.. automodule:: perturbdecode.pertdec.runTrainingComBVAE
   :members:

.. automodule:: perturbdecode.pertdec.extract_model_embeddings
   :members:

.. automodule:: perturbdecode.pertdec.selectWorkingGuides
   :members:

.. automodule:: perturbdecode.pertdec.inferEffectSizes
   :members:

.. automodule:: perturbdecode.pertdec.visualizePerturbationEmbeddings
   :members:

Models
------

.. automodule:: perturbdecode.models.CVAE_basic
   :members:

.. automodule:: perturbdecode.models.CVAE_GumbelMasked
   :members:

Data
----

.. automodule:: perturbdecode.data.ScreenDataset
   :members:

Training
--------

.. automodule:: perturbdecode.training.Training
   :members:

Utilities
---------

.. automodule:: perturbdecode.utils.Utils
   :members:

.. automodule:: perturbdecode.utils.data_utils
   :members:

.. automodule:: perturbdecode.utils.r_bridge
   :members:

.. automodule:: perturbdecode.utils.logger
   :members:

Core
----

.. automodule:: perturbdecode.core.functions
   :members:

Command line
------------

.. automodule:: perturbdecode.cli
   :members:
