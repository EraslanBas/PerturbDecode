"""Tests for the optional R integration.

Every test here is skipped when the ``[r]`` extra (rpy2 / anndata2ri) is not
installed, so the suite stays green on an R-free install.
"""

import pytest

from perturbdecode.utils.libraries import HAS_R

pytestmark = pytest.mark.skipif(not HAS_R, reason="requires the [r] extra (rpy2)")


def test_call_r_builtin_with_numpy_array():
    """A built-in R function is callable through the bridge with a numpy array."""
    import numpy as np

    from perturbdecode.utils.r_bridge import call_r_function

    result = call_r_function("sum", np.array([1, 2, 3, 4, 5]))
    assert result[0] == 15


def test_python_list_is_not_converted_to_r_vector():
    """Document a sharp edge: plain Python lists arrive in R as *lists*.

    ``numpy2ri`` converts numpy arrays to R vectors, but a bare Python list
    becomes an R ``list``, which most numeric R primitives reject. Callers
    should pass numpy arrays.
    """
    from perturbdecode.utils.r_bridge import call_r_function

    with pytest.raises(Exception, match="invalid 'type'"):
        call_r_function("sum", [1, 2, 3, 4, 5])


def test_call_r_returns_vector():
    """Vector-valued R results come back with the expected length."""
    from perturbdecode.utils.r_bridge import call_r_function

    result = call_r_function("seq_len", 4)
    assert list(result) == [1, 2, 3, 4]


def test_unknown_r_function_raises():
    """Looking up a non-existent R function fails rather than returning None."""
    from perturbdecode.utils.r_bridge import call_r_function

    with pytest.raises(Exception):
        call_r_function("this_r_function_does_not_exist_12345", 1)
