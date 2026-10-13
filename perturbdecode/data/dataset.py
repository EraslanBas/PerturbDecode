# PyTorch datasets
"""
PyTorch dataset classes.
"""

import torch
from torch.utils.data import Dataset

class ExampleDataset(Dataset):
    """
    An example PyTorch dataset.
    """
    
    def __init__(self, data, targets=None, transform=None):
        """
        Initialize dataset.
        
        Args:
            data: Input data
            targets: Target values
            transform: Data transformation function
        """
        self.data = data
        self.targets = targets
        self.transform = transform
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        x = self.data[idx]
        
        if self.transform:
            x = self.transform(x)
            
        if self.targets is not None:
            y = self.targets[idx]
            return x, y
        return x
