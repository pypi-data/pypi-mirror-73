
'''Tests for so_lazy custom function implementation'''

import unittest
from so_lazy import lazy

# pylint: disable=global-statement

TEST_DATASET = [1, 2, 3]

_DATA = []

@lazy(loader='_custom_lazy_loader')
def _default_func_no_args():
    return len(_DATA)

@lazy(loader='_custom_lazy_loader')
def _default_func_args(inc):
    return len(_DATA) + inc

@lazy(loader='_custom_lazy_loader')
def _default_func_kwargs(**kwargs):
    inc = kwargs.get('inc2', 0)
    return len(_DATA) + inc

@lazy(loader='_custom_lazy_loader')
def _default_func_args_kwargs(inc, **kwargs):
    inc = kwargs.get('inc2', 0)
    return len(_DATA) + inc

def _lazy_loader():
    raise AttributeError('Default lazy loader was called')

def _custom_lazy_loader():
    global _DATA

    if len(_DATA) == 0:
        _DATA = TEST_DATASET

class FunctionCustomLoaderTests(unittest.TestCase):
    '''Test function lazy load with custom loader'''

    def setUp(self):
        global _DATA

        _DATA = []

    @staticmethod
    def test_data_loaded_no_args():
        '''Test custom function lazy load with no args'''

        assert len(_DATA) == 0
        assert _default_func_no_args() == len(TEST_DATASET)
        assert len(_DATA) == len(TEST_DATASET)

    @staticmethod
    def test_data_loaded_args():
        '''Test custom function lazy load with args'''

        assert len(_DATA) == 0
        assert _default_func_args(0) == len(TEST_DATASET)
        assert len(_DATA) == len(TEST_DATASET)

    @staticmethod
    def test_data_loaded_kwargs():
        '''Test custom function lazy load with kwargs'''

        assert len(_DATA) == 0
        assert _default_func_kwargs(inc2=0) == len(TEST_DATASET)
        assert len(_DATA) == len(TEST_DATASET)

    @staticmethod
    def test_data_loaded_args_kwargs():
        '''Test custom function lazy load with args and kwargs'''

        assert len(_DATA) == 0
        assert _default_func_args_kwargs(0, inc2=0) == len(TEST_DATASET)
        assert len(_DATA) == len(TEST_DATASET)
