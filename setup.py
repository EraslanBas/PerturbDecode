from setuptools import setup, find_packages

setup(
    name="PerturbDecodeMulti",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "torch",
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        # Add other dependencies here
    ],
    extras_require={{
        "r": ["rpy2"],
        "dev": ["pytest", "sphinx", "sphinx_rtd_theme"],
    }},
    python_requires=">=3.8",
    package_data={
        "": ["R/*.R"],
    },
    entry_points={{
        'console_scripts': [
            'PerturbDecodeMulti=PerturbDecodeMulti.cli:main',
        ],
    }},
)
