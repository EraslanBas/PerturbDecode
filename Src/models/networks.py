# PyTorch models
"""
PyTorch neural network models.
"""

import torch
import torch.nn as nn

class ExampleModel(nn.Module):
    """An example PyTorch model."""
    
    def __init__(self, input_dim=10, hidden_dim=20, output_dim=2):
        super().__init__()
        self.layer1 = nn.Linear(input_dim, hidden_dim)
        self.layer2 = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.relu(self.layer1(x))
        return self.layer2(x)
