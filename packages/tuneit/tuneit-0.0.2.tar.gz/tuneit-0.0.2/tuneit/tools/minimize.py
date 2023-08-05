"""
High-level tools for the tunable package
"""

__all__ = [
    "minimize",
]

from .base import sample


def minimize(tunable, fnc=None, **kwargs):
    """
    Minimizes the output of the function

    Parameters
    ----------
    fnc: callable
        The function to minimize.
    variables: list of str
        Set of variables to sample.
    samples: int
        The number of samples to run. If None, all the combinations are sampled.
    kwargs: dict
        Variables passed to the compute function. See help(tunable.compute)
    """
    tunable, variables = _init(tunable, variables)
    pass
