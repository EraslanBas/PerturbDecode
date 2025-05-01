# Test models
"""
Tests for PyTorch models.
"""

import unittest
import torch
from PerturbDecodeMulti.models import ExampleModel

class TestModels(unittest.TestCase):
    
    def test_example_model(self):
        """Test the example model."""
        model = ExampleModel(input_dim=5, hidden_dim=10, output_dim=2)
        x = torch.randn(3, 5)  # Batch of 3 samples, 5 features each
        output = model(x)
        self.assertEqual(output.shape, (3, 2))  # Output should have shape [3, 2]

if __name__ == "__main__":
    unittest.main()
