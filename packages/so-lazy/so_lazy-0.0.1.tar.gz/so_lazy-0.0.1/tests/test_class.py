
'''Tests for so_lazy class implementation'''

import unittest
from so_lazy import lazy, ClassDecoratedError, NoLoaderError

# pylint: disable=too-few-public-methods

TEST_DATASET = [1, 2, 3]

class Parent:
    '''Basic class with lazy load defaults'''

    def __init__(self):
        self.data = []

    @lazy()
    def length(self):
        '''Length of internal data'''
        return len(self.data)

    @lazy()
    def length2(self):
        '''Length 2 of internal data'''
        return len(self.data)

    def _lazy_loader(self):
        if len(self.data) == 0:
            self.data = TEST_DATASET

class Child(Parent):
    '''Child class with no extensions'''

class ChildLazyLoadFunctionDisabled(Parent):
    '''Child class with no extensions but one disabled lazy
       load function'''

    @lazy(enabled=False)
    def length2(self):
        '''Override of Parent method'''
        return len(self.data)

class ChildFunctionLoader(Parent):
    '''Child class with redefined lazy function'''

    @lazy(loader='_custom_lazy_loader')
    def length2(self):
        return len(self.data)

    def _custom_lazy_loader(self):
        if len(self.data) == 0:
            self.data = TEST_DATASET + TEST_DATASET

@lazy()
class DecoratedError:
    '''Class decorated with lazy'''

class NoLazyLoader:
    '''Class without a lazy loader'''

    def __init__(self):
        self.data = []

    @lazy()
    def length(self):
        '''Length of internal data'''
        return len(self.data)

class ClassParentDefaultTests(unittest.TestCase):
    '''Test basic class lazy load with defaults'''

    def setUp(self):
        self.test_class = Parent()

    def test_data_loaded(self):
        '''Test basic class lazy load'''

        assert len(self.test_class.data) == 0
        assert self.test_class.length() == len(TEST_DATASET)
        assert len(self.test_class.data) == len(TEST_DATASET)

class ClassChildDefaultTests(unittest.TestCase):
    '''Test inherited lazy load'''

    def setUp(self):
        self.test_class = Child()

    def test_data_loaded(self):
        '''Test inherited class lazy load'''

        assert len(self.test_class.data) == 0
        assert self.test_class.length() == len(TEST_DATASET)
        assert len(self.test_class.data) == len(TEST_DATASET)

class ClassChildLazyLoadFunctionDisabledTests(unittest.TestCase):
    '''Test inherited lazy load function can be disabled'''

    def setUp(self):
        self.test_class = ChildLazyLoadFunctionDisabled()

    def test_no_data_loaded(self):
        '''Test inherited class function lazy load is disabled'''

        assert len(self.test_class.data) == 0
        assert self.test_class.length2() == 0
        assert len(self.test_class.data) == 0

    def test_data_loaded(self):
        '''Test inherited class lazy load still works for
           non-disabled functions'''

        assert len(self.test_class.data) == 0
        assert self.test_class.length() == len(TEST_DATASET)
        assert len(self.test_class.data) == len(TEST_DATASET)

class ClassChildFunctionLoaderTests(unittest.TestCase):
    '''Test inherited lazy load can be redefined per function'''

    def setUp(self):
        self.test_class = ChildFunctionLoader()

    def test_data_loaded(self):
        '''Test inherited function lazy loader not redefined'''

        assert len(self.test_class.data) == 0
        assert self.test_class.length() == len(TEST_DATASET)
        assert len(self.test_class.data) == len(TEST_DATASET)

    def test_data_custom_loaded(self):
        '''Test inherited function lazy loader redefined'''

        assert len(self.test_class.data) == 0
        assert self.test_class.length2() == len(TEST_DATASET) * 2
        assert len(self.test_class.data) == len(TEST_DATASET) * 2

class ClassErrorTests(unittest.TestCase):
    '''Test lazy errors'''

    def test_class_decorated_error(self):
        '''Test for class decorated error'''
        self.assertRaises(ClassDecoratedError, DecoratedError)

    def test_no_loader_error(self):
        '''Test for no loader error'''
        test_class = NoLazyLoader()
        self.assertRaises(NoLoaderError, test_class.length)
