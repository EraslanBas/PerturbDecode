# Test R integration
"""
Tests for R integration.
"""

import unittest
import pytest

class TestRIntegration(unittest.TestCase):
    
    @pytest.mark.skipif(not is_rpy2_available(), reason="rpy2 not available")
    def test_r_function_call(self):
        """Test calling an R function."""
        from PerturbDecodeMulti.utils.r_bridge import call_r_function
        
        # This is a simple test using R's built-in sum function
        result = call_r_function("sum", [1, 2, 3, 4, 5])
        self.assertEqual(result[0], 15)

def is_rpy2_available():
    """Check if rpy2 is available."""
    try:
        import rpy2
        return True
    except ImportError:
        return False

if __name__ == "__main__":
    unittest.main()
