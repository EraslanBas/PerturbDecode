# Command-line interface
"""
Command-line interface for the package.
"""

import argparse
import sys

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description=f'{PerturbDecodeMulti} - A Python package with R integration')
    parser.add_argument('--version', action='store_true', help='Print version information')
    # Add more command-line arguments here
    
    args = parser.parse_args()
    
    if args.version:
        from . import __version__
        print(f"{PerturbDecodeMulti} version {__version__}")
        return 0
        
    # Add more command-line functionality here
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
