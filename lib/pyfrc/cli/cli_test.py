
import os
import sys

from os.path import abspath, dirname, exists, join

import pytest

from ..wpilib import _wpilib


# TODO: setting the plugins so that the end user can invoke py.test directly
# could be a useful thing. Will have to consider that later.

class PyFrcPlugin(object):

    def __init__(self, run_fn):
        self.run_fn = run_fn
    
    def pytest_runtest_setup(self):
        _wpilib.internal.initialize_test()
    
    @pytest.fixture()
    def robot(self):
        return self.run_fn()
    
    @pytest.fixture()
    def wpilib(self):
        return _wpilib.internal

#
# Test function
#

def run(run_fn, file_location):
    


    # find test directory, change current directory so py.test can find the tests
    # -> assume that tests reside in tests or ../tests
    
    test_directory = None
    root = abspath(dirname(file_location))
    try_dirs = [join(root, 'tests'), abspath(join(root, '..', 'tests'))]
    
    for d in try_dirs:
        if exists(d):
            test_directory = d
            break
    
    if test_directory is None:
        print("Could not find tests directory! Looked in %s" % try_dirs)
        return 1
    
    os.chdir(test_directory)
    
    return pytest.main(sys.argv[1:], plugins=[PyFrcPlugin(run_fn)])
    
    # need to reset wpilib internal state inbetween each test?
    
    # need to setup robot/wpilib fixtures
    
    #