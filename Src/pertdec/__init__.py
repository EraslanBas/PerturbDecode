# PerturbDecodeMulti package
"""
PerturbDecodeMulti - API
"""

__version__ = '0.1.0'


# Import API functions from submodules
from .runTrainingComBVAE import runTrainingComBVAE
from .createTrainValData import createTrainValData
from .extract_model_embeddings import extract_model_embeddings
from .visualizePerturbationEmbeddings import visualizePerturbationEmbeddings
from .selectWorkingGuides import selectWorkingGuides
from .inferEffectSizes import inferEffectSizes

# Re-export the functions to make them available directly from api
__all__ = [
    "runTrainingComBVAE",
    "createTrainValData",
    "extract_model_embeddings",
    "visualizePerturbationEmbeddings",
    "selectWorkingGuides",
    "inferEffectSizes"
    # Add other API functions
]

# Version information
__version__ = '0.1.0'