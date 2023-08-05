
'''Tests for so_lazy package'''

import unittest
import os

import so_lazy

class PackageVarTests(unittest.TestCase):
    '''Test package variables are set'''

    @staticmethod
    def test_author():
        '''Package info author exists'''
        assert so_lazy.__author__ is not None

    @staticmethod
    def test_homepage():
        '''Package info homepage exists'''
        assert so_lazy.__homepage__ is not None

    @staticmethod
    def test_download():
        '''Package info download exists'''
        assert so_lazy.__download__ is not None

    @staticmethod
    def test_license():
        '''Package info license exists'''
        assert so_lazy.__license__ is not None

    @staticmethod
    def test_description():
        '''Package info description exists'''
        assert so_lazy.__description__ is not None

    @staticmethod
    def test_version():
        '''Package info version exists'''
        assert so_lazy.__version__ is not None

    @staticmethod
    def test_long_description():
        '''Package info long description exists'''
        assert os.path.isfile('./README.md')
