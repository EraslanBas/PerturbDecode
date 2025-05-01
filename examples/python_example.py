# Python example
"""
Example of using the package from Python.
"""

import torch
import numpy as np
from PerturbDecodeMulti.models import ExampleModel
from PerturbDecodeMulti.utils import numpy_to_tensor

def main():
    # Create a random dataset
    data = np.random.randn(100, 10)
    
    # Convert to PyTorch tensor
    tensor_data = numpy_to_tensor(data)
    
    # Create and use a model
    model = ExampleModel(input_dim=10, hidden_dim=20, output_dim=2)
    output = model(tensor_data)
    
    print(f"Model output shape: {output.shape}")
    print(f"First few predictions:\n{output[:5]}")

if __name__ == "__main__":
    main()
