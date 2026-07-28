# R integration utilities
"""
Bridge functions for R integration.
"""

def call_r_function(r_function, *args, **kwargs):
    """Call an R function from Python via rpy2.

    Parameters
    ----------
    r_function : str
        Name of the R function to call, looked up in R's global environment
        (e.g. ``"sum"``, ``"seq_len"``).
    \\*args, \\*\\*kwargs
        Arguments forwarded to the R function.

    Returns
    -------
    rpy2.robjects.RObject
        The value returned by the R function.

    Raises
    ------
    ImportError
        If ``rpy2`` is not installed. Install the optional extra with
        ``pip install 'PerturbDecode[r]'``.

    Notes
    -----
    numpy arrays are converted to R vectors by ``numpy2ri``, but a plain
    Python ``list`` arrives in R as a ``list``, which most numeric R
    primitives reject. Pass ``numpy.ndarray`` for vector arguments.

    Examples
    --------
    >>> import numpy as np
    >>> call_r_function("sum", np.array([1, 2, 3]))[0]
    6
    """
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
