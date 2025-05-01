# Test core functionality
"""
Tests for core functionality.
"""

import unittest
from PerturbDecodeMulti.core import example_function

class TestCore(unittest.TestCase):
    
    def test_example_function(self):
        """Test the example function."""
        result = example_function()
        self.assertEqual(result, "This is an example function")

if __name__ == "__main__":
    unittest.main()
