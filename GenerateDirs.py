#!/usr/bin/env python3
"""
Script to generate a template directory structure for a Python package that 
integrates R and Python with PyTorch code.
"""

import os
import sys
import argparse
from pathlib import Path


def create_file(path, content=""):
    """Create a file with optional content."""
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created: {path}")


def generate_structure(base_dir, package_name):
    """Generate the full package directory structure."""
    base_path = Path(base_dir) / package_name
    
    # Create root directory
    os.makedirs(base_path, exist_ok=True)
    
    # Create directories
    directories = [
        ".github/workflows",
        "R",
        f"{package_name}/core",
        f"{package_name}/models",
        f"{package_name}/utils",
        f"{package_name}/data",
        "tests",
        "examples",
        "docs",
    ]
    
    for directory in directories:
        os.makedirs(base_path / directory, exist_ok=True)
        
    # Create Python package files
    create_file(base_path / f"{package_name}/__init__.py", f"""# {package_name} package
\"\"\"
{package_name} - A Python package with R integration and PyTorch models
\"\"\"

__version__ = '0.1.0'
""")
    
    create_file(base_path / f"{package_name}/core/__init__.py", "from .functions import *")
    create_file(base_path / f"{package_name}/core/functions.py", """# Core functionality
\"\"\"
Core functions for the package.
\"\"\"

def example_function():
    \"\"\"An example function.\"\"\"
    return "This is an example function"
""")
    
    create_file(base_path / f"{package_name}/models/__init__.py", "from .networks import *")
    create_file(base_path / f"{package_name}/models/networks.py", """# PyTorch models
\"\"\"
PyTorch neural network models.
\"\"\"

import torch
import torch.nn as nn

class ExampleModel(nn.Module):
    \"\"\"An example PyTorch model.\"\"\"
    
    def __init__(self, input_dim=10, hidden_dim=20, output_dim=2):
        super().__init__()
        self.layer1 = nn.Linear(input_dim, hidden_dim)
        self.layer2 = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.relu(self.layer1(x))
        return self.layer2(x)
""")
    
    create_file(base_path / f"{package_name}/utils/__init__.py", "from .r_bridge import *\nfrom .data_utils import *")
    create_file(base_path / f"{package_name}/utils/r_bridge.py", """# R integration utilities
\"\"\"
Bridge functions for R integration.
\"\"\"

def call_r_function(r_function, *args, **kwargs):
    \"\"\"
    Call an R function from Python.
    
    This is a placeholder. You'll need to implement this using rpy2 or another
    Python-R bridge.
    
    Args:
        r_function (str): Name of the R function to call
        *args, **kwargs: Arguments to pass to the R function
        
    Returns:
        Result from the R function
    \"\"\"
    try:
        import rpy2.robjects as robjects
        from rpy2.robjects.packages import importr
        
        # Load the package that contains the function
        # This is just an example and would need to be customized
        base = importr('base')
        
        # Call the R function
        r_func = robjects.r[r_function]
        result = r_func(*args, **kwargs)
        
        return result
    except ImportError:
        raise ImportError("rpy2 is required for R integration. Install it with pip install rpy2")
""")
    
    create_file(base_path / f"{package_name}/utils/data_utils.py", """# Data handling utilities
\"\"\"
Utilities for data handling and preprocessing.
\"\"\"

import numpy as np
import torch

def numpy_to_tensor(data):
    \"\"\"
    Convert numpy array to PyTorch tensor.
    
    Args:
        data (numpy.ndarray): Input numpy array
        
    Returns:
        torch.Tensor: PyTorch tensor
    \"\"\"
    return torch.from_numpy(data).float()
""")
    
    create_file(base_path / f"{package_name}/data/__init__.py", "from .dataset import *")
    create_file(base_path / f"{package_name}/data/dataset.py", """# PyTorch datasets
\"\"\"
PyTorch dataset classes.
\"\"\"

import torch
from torch.utils.data import Dataset

class ExampleDataset(Dataset):
    \"\"\"
    An example PyTorch dataset.
    \"\"\"
    
    def __init__(self, data, targets=None, transform=None):
        \"\"\"
        Initialize dataset.
        
        Args:
            data: Input data
            targets: Target values
            transform: Data transformation function
        \"\"\"
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
""")
    
    create_file(base_path / f"{package_name}/cli.py", """# Command-line interface
\"\"\"
Command-line interface for the package.
\"\"\"

import argparse
import sys

def main():
    \"\"\"Main entry point for the CLI.\"\"\"
    parser = argparse.ArgumentParser(description=f'{package_name} - A Python package with R integration')
    parser.add_argument('--version', action='store_true', help='Print version information')
    # Add more command-line arguments here
    
    args = parser.parse_args()
    
    if args.version:
        from . import __version__
        print(f"{package_name} version {__version__}")
        return 0
        
    # Add more command-line functionality here
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
""".replace("package_name", package_name))
    
    # Create R files
    create_file(base_path / "R/__init__.R", """# Package initialization
#' @export

.onLoad <- function(libname, pkgname) {
  # Initialization code here
}
""")
    
    create_file(base_path / "R/functions.R", """# R functions for the package

#' Example R function
#'
#' @param x Numeric input
#' @return x squared
#' @export
example_r_function <- function(x) {
  return(x^2)
}
""")
    
    # Create test files
    create_file(base_path / "tests/__init__.py", "# Tests package")
    create_file(base_path / "tests/test_core.py", """# Test core functionality
\"\"\"
Tests for core functionality.
\"\"\"

import unittest
from {package_name}.core import example_function

class TestCore(unittest.TestCase):
    
    def test_example_function(self):
        \"\"\"Test the example function.\"\"\"
        result = example_function()
        self.assertEqual(result, "This is an example function")

if __name__ == "__main__":
    unittest.main()
""".replace("{package_name}", package_name))
    
    create_file(base_path / "tests/test_models.py", """# Test models
\"\"\"
Tests for PyTorch models.
\"\"\"

import unittest
import torch
from {package_name}.models import ExampleModel

class TestModels(unittest.TestCase):
    
    def test_example_model(self):
        \"\"\"Test the example model.\"\"\"
        model = ExampleModel(input_dim=5, hidden_dim=10, output_dim=2)
        x = torch.randn(3, 5)  # Batch of 3 samples, 5 features each
        output = model(x)
        self.assertEqual(output.shape, (3, 2))  # Output should have shape [3, 2]

if __name__ == "__main__":
    unittest.main()
""".replace("{package_name}", package_name))
    
    create_file(base_path / "tests/test_r_integration.py", """# Test R integration
\"\"\"
Tests for R integration.
\"\"\"

import unittest
import pytest

class TestRIntegration(unittest.TestCase):
    
    @pytest.mark.skipif(not is_rpy2_available(), reason="rpy2 not available")
    def test_r_function_call(self):
        \"\"\"Test calling an R function.\"\"\"
        from {package_name}.utils.r_bridge import call_r_function
        
        # This is a simple test using R's built-in sum function
        result = call_r_function("sum", [1, 2, 3, 4, 5])
        self.assertEqual(result[0], 15)

def is_rpy2_available():
    \"\"\"Check if rpy2 is available.\"\"\"
    try:
        import rpy2
        return True
    except ImportError:
        return False

if __name__ == "__main__":
    unittest.main()
""".replace("{package_name}", package_name))
    
    # Create example files
    create_file(base_path / "examples/python_example.py", """# Python example
\"\"\"
Example of using the package from Python.
\"\"\"

import torch
import numpy as np
from {package_name}.models import ExampleModel
from {package_name}.utils import numpy_to_tensor

def main():
    # Create a random dataset
    data = np.random.randn(100, 10)
    
    # Convert to PyTorch tensor
    tensor_data = numpy_to_tensor(data)
    
    # Create and use a model
    model = ExampleModel(input_dim=10, hidden_dim=20, output_dim=2)
    output = model(tensor_data)
    
    print(f"Model output shape: {output.shape}")
    print(f"First few predictions:\\n{output[:5]}")

if __name__ == "__main__":
    main()
""".replace("{package_name}", package_name))
    
    create_file(base_path / "examples/r_example.R", """# R example
#
# Example of using the package from R
#

# Source the R functions
source("../R/functions.R")

# Use an R function
result <- example_r_function(5)
print(paste("Result:", result))

# Example of calling Python from R using reticulate
# Uncomment if you have reticulate installed
# library(reticulate)
# py <- import("{package_name}")
# # Call Python functions here
""".replace("{package_name}", package_name))
    
    # Create documentation files
    create_file(base_path / "docs/conf.py", """# Configuration file for the Sphinx documentation builder.

project = '{package_name}'
copyright = '2025'
author = 'Your Name'

# The full version, including alpha/beta/rc tags
release = '0.1.0'

# Add any Sphinx extension module names here
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

# Add any paths that contain templates here
templates_path = ['_templates']

# List of patterns to exclude from source files
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The theme to use for HTML and HTML Help pages
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files
html_static_path = ['_static']
""".replace("{package_name}", package_name))
    
    create_file(base_path / "docs/index.rst", """Welcome to {package_name}'s documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
""".replace("{package_name}", package_name))
    
    create_file(base_path / "docs/api.rst", """API Reference
============

Core
----

.. automodule:: {package_name}.core.functions
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

.. automodule:: {package_name}.models.networks
   :members:
   :undoc-members:
   :show-inheritance:

Utilities
---------

.. automodule:: {package_name}.utils.r_bridge
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: {package_name}.utils.data_utils
   :members:
   :undoc-members:
   :show-inheritance:

Data
----

.. automodule:: {package_name}.data.dataset
   :members:
   :undoc-members:
   :show-inheritance:
""".replace("{package_name}", package_name))
    
    # Create GitHub workflow
    create_file(base_path / ".github/workflows/python-package.yml", """name: Python Package

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install R
      uses: r-lib/actions/setup-r@v2
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install pytest pytest-cov
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install -e .
    - name: Test with pytest
      run: |
        pytest --cov={package_name} --cov-report=xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
""".replace("{package_name}", package_name))
    
    # Create configuration and setup files
    create_file(base_path / ".gitignore", """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
dist/
build/
*.egg-info/

# Unit test / coverage reports
.coverage
htmlcov/
.pytest_cache/

# Sphinx documentation
docs/_build/

# Jupyter Notebook
.ipynb_checkpoints

# Virtual environments
venv/
env/
ENV/

# IDE specific files
.idea/
.vscode/
*.swp
*.swo

# OS specific files
.DS_Store
Thumbs.db
""")
    
    create_file(base_path / "LICENSE", """MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")
    
    create_file(base_path / "MANIFEST.in", """include LICENSE
include README.md
include requirements.txt
recursive-include R *
recursive-include examples *
""")
    
    create_file(base_path / "pyproject.toml", """[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py38']

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
""")
    
    create_file(base_path / "setup.py", """from setuptools import setup, find_packages

setup(
    name="{package_name}",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "torch",
        # Add other dependencies here
    ],
    extras_require={{
        "r": ["rpy2"],
        "dev": ["pytest", "sphinx", "sphinx_rtd_theme"],
    }},
    entry_points={{
        'console_scripts': [
            '{package_name}={package_name}.cli:main',
        ],
    }},
)
""".replace("{package_name}", package_name))
    
    create_file(base_path / "setup.cfg", """[metadata]
name = {package_name}
version = 0.1.0
description = A Python package with R integration and PyTorch models
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/yourusername/{package_name}
author = Your Name
author_email = your.email@example.com
license = MIT
classifiers =
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: 3.10
    License :: OSI Approved :: MIT License

[options]
packages = find:
python_requires = >=3.8
""".replace("{package_name}", package_name))
    
    create_file(base_path / "requirements.txt", """numpy>=1.20.0
torch>=1.9.0
# rpy2>=3.4.0  # Uncomment if you need R integration
pytest>=6.0.0
sphinx>=4.0.0
sphinx_rtd_theme>=0.5.0
""")
    
    create_file(base_path / "environment.yml", """name: {package_name}
channels:
  - pytorch
  - conda-forge
  - defaults
dependencies:
  - python>=3.8
  - numpy>=1.20.0
  - pytorch>=1.9.0
  - r-base>=4.0  # R language
  - pip
  - pip:
    - pytest>=6.0.0
    - sphinx>=4.0.0
    - sphinx_rtd_theme>=0.5.0
    # - rpy2>=3.4.0  # Uncomment if you need R integration
""".replace("{package_name}", package_name))
    
    create_file(base_path / "README.md", """# {package_name}

A Python package with R integration and PyTorch models.

## Installation

### Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/{package_name}.git
cd {package_name}

# Install in development mode
pip install -e .

# If you need R integration
pip install -e ".[r]"

# If you need development tools
pip install -e ".[dev]"
```

### Using Conda

```bash
# Create conda environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate {package_name}

# Install the package
pip install -e .
```

## Features

- Integrated R and Python functionality
- PyTorch model definitions
- Easy-to-use data processing utilities
- Command-line interface

## Examples

See the `examples/` directory for usage examples.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov={package_name}
```

## Documentation

Build the documentation:

```bash
cd docs
make html
```

Then open `_build/html/index.html` in your browser.

## License

MIT
""".replace("{package_name}", package_name))
    
    print(f"\nPackage structure created at: {base_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate a template directory structure for a Python package with R integration.')
    parser.add_argument('package_name', help='Name of the package')
    parser.add_argument('--output-dir', '-o', default='.', 
                      help='Output directory (default: current directory)')
    
    args = parser.parse_args()
    
    generate_structure(args.output_dir, args.package_name)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())