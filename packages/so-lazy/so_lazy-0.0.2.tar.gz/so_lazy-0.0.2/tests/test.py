#!/usr/bin/env python

'''Test runner'''

import os.path
import sys
import unittest

if __name__ == '__main__':
    sys.path.insert(0, os.path.realpath('..'))

    suites = unittest.defaultTestLoader.discover('.', 'test*.py')

    if not unittest.TextTestRunner(verbosity=2).run(suites).wasSuccessful():
        sys.exit(1)
