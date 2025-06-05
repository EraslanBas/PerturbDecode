#!/usr/bin/env python3
"""
Script to generate the PyRRegression package structure.
This package demonstrates R integration with Python for linear regression.
"""

import os
import sys
from pathlib import Path


def create_file(path, content=""):
    """Create a file with optional content."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created: {path}")


def generate_pyrregression_package(base_dir):
    """Generate the PyRRegression package with R integration."""
    base_path = Path(base_dir) / "pyrregression"
    
    # Create directories structure
    directories = [
        "R",
        "pyrregression",
        "pyrregression/core",
        "pyrregression/utils",
        "pyrregression/models",
        "tests",
        "examples",
        "docs",
    ]
    
    for directory in directories:
        os.makedirs(base_path / directory, exist_ok=True)
    
    # Create R scripts
    create_file(base_path / "R/linear_model.R", """# R script for linear regression

#' Fit a linear regression model
#'
#' @param data A data frame containing the variables in the model
#' @param formula A formula specifying the model
#' @param ... Additional arguments to pass to lm
#' @return A list containing model coefficients, fitted values, residuals, and summary statistics
#' @export
fit_linear_model <- function(data, formula = "y ~ x1 + x2", ...) {
  # Ensure the input is a data frame
  data <- as.data.frame(data)
  
  # Fit the model
  model <- lm(formula = formula, data = data, ...)
  
  # Extract useful information
  coefficients <- coef(model)
  fitted_values <- fitted(model)
  residuals <- residuals(model)
  
  # Get summary statistics
  model_summary <- summary(model)
  r_squared <- model_summary$r.squared
  adj_r_squared <- model_summary$adj.r.squared
  f_statistic <- model_summary$fstatistic
  p_value <- pf(f_statistic[1], f_statistic[2], f_statistic[3], lower.tail = FALSE)
  
  # Get coefficient p-values
  coef_summary <- summary(model)$coefficients
  coef_p_values <- coef_summary[, 4]
  
  # Return results as a list
  return(list(
    coefficients = coefficients,
    fitted_values = fitted_values,
    residuals = residuals,
    r_squared = r_squared,
    adj_r_squared = adj_r_squared,
    f_statistic = f_statistic,
    p_value = p_value,
    coef_p_values = coef_p_values
  ))
}

#' Predict using a linear model
#'
#' @param model A linear model object
#' @param newdata A data frame containing the predictor variables
#' @return A vector of predicted values
#' @export
predict_linear_model <- function(model, newdata) {
  # Ensure the input is a data frame
  newdata <- as.data.frame(newdata)
  
  # Make predictions
  predictions <- predict(model, newdata)
  
  return(predictions)
}
""")
    
    # Create Python package files
    create_file(base_path / "pyrregression/__init__.py", """# PyRRegression package
\"\"\"
PyRRegression - A Python package that integrates with R for regression analysis
\"\"\"

from .core.regression import fit_regression, predict_regression

__version__ = '0.1.0'
""")
    
    create_file(base_path / "pyrregression/core/__init__.py", """# Core functionality
from .regression import *
""")
    
    create_file(base_path / "pyrregression/core/regression.py", """# Regression functionality
\"\"\"
Core regression functions that integrate with R.
\"\"\"

import pandas as pd
import numpy as np
from ..utils.r_bridge import call_r_function

def fit_regression(data_path, formula="y ~ x1 + x2"):
    \"\"\"
    Fit a linear regression model using R.
    
    Args:
        data_path (str): Path to the CSV file with columns x1, x2, and y
        formula (str, optional): R formula for the model. Defaults to "y ~ x1 + x2".
    
    Returns:
        dict: Dictionary containing model results
    \"\"\"
    # Read the CSV file
    df = pd.read_csv(data_path)
    
    # Ensure the required columns exist
    required_cols = ['x1', 'x2', 'y']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Call the R function to fit the model
    r_result = call_r_function("fit_linear_model", df, formula)
    
    # Convert R result to Python dictionary
    result = {
        'coefficients': {
            'intercept': r_result[0]['coefficients'][0],
            'x1': r_result[0]['coefficients'][1],
            'x2': r_result[0]['coefficients'][2]
        },
        'fitted_values': np.array(r_result[0]['fitted_values']),
        'residuals': np.array(r_result[0]['residuals']),
        'r_squared': r_result[0]['r_squared'][0],
        'adj_r_squared': r_result[0]['adj_r_squared'][0],
        'f_statistic': r_result[0]['f_statistic'][0],
        'p_value': r_result[0]['p_value'][0],
        'coef_p_values': {
            'intercept': r_result[0]['coef_p_values'][0],
            'x1': r_result[0]['coef_p_values'][1],
            'x2': r_result[0]['coef_p_values'][2]
        }
    }
    
    return result

def predict_regression(model, new_data):
    \"\"\"
    Make predictions using a fitted linear regression model.
    
    Args:
        model (dict): Model dictionary from fit_regression
        new_data (pd.DataFrame or str): New data as DataFrame or path to CSV
    
    Returns:
        np.ndarray: Predicted values
    \"\"\"
    # Handle new_data as path or DataFrame
    if isinstance(new_data, str):
        new_data = pd.read_csv(new_data)
    
    # Ensure required columns exist
    required_cols = ['x1', 'x2']
    missing_cols = [col for col in required_cols if col not in new_data.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Calculate predictions manually using the model coefficients
    predictions = (
        model['coefficients']['intercept'] +
        model['coefficients']['x1'] * new_data['x1'] +
        model['coefficients']['x2'] * new_data['x2']
    )
    
    return predictions.values
""")
    
    create_file(base_path / "pyrregression/utils/__init__.py", """# Utilities package
from .r_bridge import *
from .data_utils import *
""")
    
    create_file(base_path / "pyrregression/utils/r_bridge.py", """# R integration utilities
\"\"\"
Bridge functions for R integration using rpy2.
\"\"\"

import os
import pandas as pd
import numpy as np

def call_r_function(r_function_name, *args, **kwargs):
    \"\"\"
    Call an R function from Python using rpy2.
    
    Args:
        r_function_name (str): Name of the R function to call
        *args, **kwargs: Arguments to pass to the R function
        
    Returns:
        Result from the R function
    \"\"\"
    try:
        import rpy2.robjects as robjects
        from rpy2.robjects import pandas2ri
        from rpy2.robjects.conversion import localconverter
        from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
        
        # Source the R script
        r_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                 "R", "linear_model.R")
        with open(r_file_path, 'r') as file:
            r_code = file.read()
        
        # Create an R package with the functions from the R script
        r_package = SignatureTranslatedAnonymousPackage(r_code, "r_package")
        
        # Get the R function
        r_func = getattr(r_package, r_function_name)
        
        # Handle data frame conversion
        if args and isinstance(args[0], pd.DataFrame):
            with localconverter(robjects.default_converter + pandas2ri.converter):
                r_df = robjects.conversion.py2rpy(args[0])
                # Replace the first argument with the converted DataFrame
                args = (r_df,) + args[1:]
        
        # Call the R function
        result = r_func(*args, **kwargs)
        
        return result
        
    except ImportError:
        raise ImportError("rpy2 is required for R integration. Install it with pip install rpy2")
""")
    
    create_file(base_path / "pyrregression/utils/data_utils.py", """# Data utilities
\"\"\"
Utilities for data handling.
\"\"\"

import pandas as pd
import numpy as np

def generate_sample_data(n_samples=100, seed=42, output_path=None):
    \"\"\"
    Generate sample data for regression.
    
    Args:
        n_samples (int, optional): Number of samples. Defaults to 100.
        seed (int, optional): Random seed. Defaults to 42.
        output_path (str, optional): Path to save the CSV. If None, returns DataFrame.
        
    Returns:
        pd.DataFrame or None: Generated data or None if saved to file
    \"\"\"
    # Set random seed
    np.random.seed(seed)
    
    # Generate predictor variables
    x1 = np.random.normal(0, 1, n_samples)
    x2 = np.random.normal(0, 1, n_samples)
    
    # Generate response with some noise
    # y = 2 + 0.8*x1 + 1.2*x2 + noise
    noise = np.random.normal(0, 0.5, n_samples)
    y = 2 + 0.8 * x1 + 1.2 * x2 + noise
    
    # Create DataFrame
    df = pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'y': y
    })
    
    # Save to file if output_path is provided
    if output_path:
        df.to_csv(output_path, index=False)
        return None
    
    return df
""")
    
    create_file(base_path / "pyrregression/models/__init__.py", """# Models package
\"\"\"
This directory is for more complex model implementations.
\"\"\"
""")
    
    # Create examples
    create_file(base_path / "examples/regression_example.py", """#!/usr/bin/env python3
\"\"\"
Example of using PyRRegression to fit a linear regression model.
\"\"\"

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add the package root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyrregression import fit_regression, predict_regression
from pyrregression.utils.data_utils import generate_sample_data

def main():
    # Generate sample data
    data_path = 'sample_data.csv'
    generate_sample_data(n_samples=100, output_path=data_path)
    print(f"Generated sample data: {data_path}")
    
    # Fit regression model
    print("Fitting regression model...")
    model = fit_regression(data_path)
    
    # Print results
    print("\\nRegression Results:")
    print(f"Coefficients: {model['coefficients']}")
    print(f"R-squared: {model['r_squared']:.4f}")
    print(f"Adjusted R-squared: {model['adj_r_squared']:.4f}")
    print(f"F-statistic: {model['f_statistic']:.4f}")
    print(f"p-value: {model['p_value']:.6f}")
    print("\\nCoefficient p-values:")
    for coef, p_val in model['coef_p_values'].items():
        print(f"  {coef}: {p_val:.6f}")
    
    # Generate new data for prediction
    new_data = pd.DataFrame({
        'x1': np.random.normal(0, 1, 10),
        'x2': np.random.normal(0, 1, 10)
    })
    
    # Make predictions
    print("\\nMaking predictions on new data...")
    predictions = predict_regression(model, new_data)
    
    # Print predictions
    print("\\nPredictions:")
    for i, pred in enumerate(predictions):
        print(f"  Sample {i+1}: {pred:.4f}")
    
    # Clean up
    if os.path.exists(data_path):
        os.remove(data_path)
        print(f"\\nRemoved sample data file: {data_path}")

if __name__ == "__main__":
    main()
""")
    
    # Create test files
    create_file(base_path / "tests/__init__.py", "# Tests package")
    
    create_file(base_path / "tests/test_regression.py", """# Test regression
\"\"\"
Tests for regression functionality.
\"\"\"

import os
import sys
import unittest
import tempfile
import pandas as pd
import numpy as np

# Add the package root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyrregression import fit_regression, predict_regression
from pyrregression.utils.data_utils import generate_sample_data

class TestRegression(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary file for the test data
        self.test_file = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        self.test_file.close()
        
        # Generate test data
        generate_sample_data(n_samples=50, seed=123, output_path=self.test_file.name)
    
    def tearDown(self):
        # Remove temporary file
        if os.path.exists(self.test_file.name):
            os.remove(self.test_file.name)
    
    def test_fit_regression(self):
        # Test fitting regression model
        try:
            model = fit_regression(self.test_file.name)
            
            # Check that all expected keys are present
            expected_keys = ['coefficients', 'fitted_values', 'residuals', 'r_squared', 
                             'adj_r_squared', 'f_statistic', 'p_value', 'coef_p_values']
            self.assertTrue(all(key in model for key in expected_keys))
            
            # Check coefficients (should be close to the data generation parameters)
            self.assertAlmostEqual(model['coefficients']['intercept'], 2.0, delta=0.5)
            self.assertAlmostEqual(model['coefficients']['x1'], 0.8, delta=0.5)
            self.assertAlmostEqual(model['coefficients']['x2'], 1.2, delta=0.5)
            
            # R-squared should be high for this simulated data
            self.assertGreater(model['r_squared'], 0.7)
            
            print("Regression model fitted successfully")
            
        except ImportError:
            print("Skipping test_fit_regression because rpy2 is not installed")
    
    def test_predict_regression(self):
        # Create a mock model
        mock_model = {
            'coefficients': {
                'intercept': 2.0,
                'x1': 0.8,
                'x2': 1.2
            }
        }
        
        # Create test data
        test_data = pd.DataFrame({
            'x1': [1.0, 2.0],
            'x2': [1.0, 2.0]
        })
        
        # Manually calculate expected predictions
        expected = np.array([4.0, 5.6])  # 2.0 + 0.8*x1 + 1.2*x2
        
        # Get predictions
        predictions = predict_regression(mock_model, test_data)
        
        # Check predictions
        np.testing.assert_almost_equal(predictions, expected)
        
        print("Predictions calculated correctly")

if __name__ == "__main__":
    unittest.main()
""")
    
    # Create setup and configuration files
    create_file(base_path / "setup.py", """from setuptools import setup, find_packages

setup(
    name="pyrregression",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        # rpy2 is a conditional dependency
    ],
    extras_require={
        "r": ["rpy2>=3.4.0"],
        "dev": ["pytest>=6.0.0"],
    },
    python_requires=">=3.8",
    package_data={
        "": ["R/*.R"],
    },
)
""")
    
    create_file(base_path / "README.md", """# PyRRegression

A Python package that integrates with R for regression analysis.

## Features

- Read CSV data and perform linear regression using R
- Seamless integration between Python and R
- Easy-to-use API for regression analysis

## Installation

```bash
# Clone the repository
git clone https://github.com/username/pyrregression.git
cd pyrregression

# Install the package
pip install -e .

# If you need R integration
pip install -e ".[r]"
```

### Requirements

- Python 3.8+
- R 4.0+
- Required R packages: stats
- Required Python packages: numpy, pandas, rpy2

## Usage

```python
from pyrregression import fit_regression, predict_regression

# Fit a regression model
model = fit_regression('data.csv')

# Print results
print(f"Coefficients: {model['coefficients']}")
print(f"R-squared: {model['r_squared']}")

# Make predictions
import pandas as pd
new_data = pd.DataFrame({
    'x1': [1.0, 2.0],
    'x2': [1.0, 2.0]
})
predictions = predict_regression(model, new_data)
print(f"Predictions: {predictions}")
```

## Example

Check the `examples/regression_example.py` script for a complete example of using the package.

## License

MIT
""")

    create_file(base_path / "requirements.txt", """numpy>=1.20.0
pandas>=1.3.0
matplotlib>=3.4.0
# rpy2>=3.4.0  # Uncomment if you need R integration
pytest>=6.0.0
""")

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

# Generated data files
*.csv
""")
    
    print(f"\nPyRRegression package created at: {base_path}")
    print("\nThis package demonstrates R integration with Python for linear regression.")
    print("\nKey components:")
    print("1. R/linear_model.R - R functions for linear regression")
    print("2. pyrregression/core/regression.py - Python interface to R functions")
    print("3. pyrregression/utils/r_bridge.py - Bridge between Python and R using rpy2")
    print("4. examples/regression_example.py - Example script showing usage")
    print("\nTo use this package:")
    print("1. Ensure R is installed on your system")
    print("2. Install the package with pip install -e \".[r]\"")
    print("3. Run the example script: python examples/regression_example.py")


# Create a sample dataset for demonstration
def generate_sample_dataset():
    """Generate a sample CSV dataset for testing the package."""
    
    sample_csv = """x1,x2,y
1.2,2.3,6.5
0.5,1.8,4.9
2.1,0.9,5.1
-0.3,1.2,2.8
1.5,-0.5,2.4
-1.2,-0.8,0.1
0.8,2.2,5.8
1.9,1.7,6.2
-0.6,0.5,1.5
1.1,1.3,4.6
"""
    
    return sample_csv


if __name__ == "__main__":
    # The main entry point if the script is run directly
    if len(sys.argv) < 2:
        print("Usage: python generate_pyrregression.py <output_directory>")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    generate_pyrregression_package(output_dir)
    
    # Generate a sample dataset file
    sample_data_path = os.path.join(output_dir, "pyrregression", "sample_data.csv")
    with open(sample_data_path, 'w') as f:
        f.write(generate_sample_dataset())
    print(f"Created sample dataset: {sample_data_path}")