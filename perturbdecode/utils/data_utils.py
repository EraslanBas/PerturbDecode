# Data handling utilities
"""
Utilities for data handling and preprocessing.
"""

import numpy as np
import torch

def numpy_to_tensor(data):
    """
    Convert numpy array to PyTorch tensor.
    
    Args:
        data (numpy.ndarray): Input numpy array
        
    Returns:
        torch.Tensor: PyTorch tensor
    """
    return torch.from_numpy(data).float()
