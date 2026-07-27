# PerturbDecodeMulti

A Python package with R integration and PyTorch models.

## Installation

### Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/PerturbDecodeMulti.git
cd PerturbDecodeMulti

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
conda activate PerturbDecodeMulti

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
pytest --cov=PerturbDecodeMulti
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
