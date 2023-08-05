""" Test suite for navis.

Examples
--------

From terminal:
$ cd folder/to/navis
$ pytest

From shell:
>>> import unittest
>>> from navis.tests import test
>>> suite = unittest.TestLoader().loadTestsFromModule(test)
>>> unittest.TextTestRunner().run(suite)

"""

import unittest
import warnings
import navis


try:
    import igraph  # type: ignore
except BaseException:
    igraph = None
    warnings.warn('iGraph library not found. Will test only with NetworkX.')

import doctest

# Set navis to headless -> this prevents viewer window from showing
from navis import config
config.headless = True


def try_conditions(func):
    """Runs each test under various conditions and asserts that results
    are always the same."""

    def wrapper(*args, **kwargs):
        navis.config.use_igraph = False
        res1 = func(*args, **kwargs)
        if igraph:
            navis.config.use_igraph = True
            res2 = func(*args, **kwargs)
            assert res1 == res2
        return res1
    return wrapper


@try_conditions
def test_load_data():
    doctest.testmod(navis.data.load_data,
                    raise_on_error=False,
                    globs={'navis': navis})


@try_conditions
def test_vispy_viewer():
    doctest.testmod(navis.plotting.vispy.viewer,
                    raise_on_error=False,
                    globs={'navis': navis})
