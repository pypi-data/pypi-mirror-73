import inspect
import logging
import os
import pytest
from rstdepassuredtchnq.core.base.apihelpers.common_methods import CommonMethods

from rstdepassuredtchnq.core.base.log.Base_Logging import Base_Logging

cur_path = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "/results/log")

calling_module = None


@pytest.fixture(scope="module")
def log_obj(testname):
    import pathlib
    actual_path = pathlib.Path().absolute()
    common = CommonMethods()
    log_obj = set_log_file(actual_path)
    log_obj.write(actual_path)
    log_obj.write(
        '\n\n\n****************************************** Started Test Execution ******************************************')
    yield log_obj
    common.make_dir('%s/../results/screenshots' % actual_path)
    log_obj.write_test_summary()


@pytest.fixture(scope="module")
def testname(request):
    "pytest fixture for testname"
    name_of_test = request.node.name
    name_of_test = name_of_test.split('[')[0]

    return name_of_test


def set_calling_module(name):
    "Set the test name"
    calling_module = name


def get_calling_module():
    "Get the name of the calling module"
    if calling_module is None:
        # Try to intelligently figure out name of test when not using pytest
        full_stack = inspect.stack()
        index = -1
        for stack_frame in full_stack:
            print(stack_frame[1], stack_frame[3])
            # stack_frame[1] -> file name
            # stack_frame[3] -> method
            if 'test_' in stack_frame[1]:
                index = full_stack.index(stack_frame)
                break
        test_file = full_stack[index][1]
        test_file = test_file.split(os.sep)[-1]
        testname = test_file.split('.py')[0]
        set_calling_module(testname)

    return calling_module


def get_test_name():
    testname = "TestExecution"
    return testname


def set_log_file(filepath):
    'set the log file'
    actual_test_name = get_calling_module()
    print(' --------- Get Log File %s' % actual_test_name)

    test_name = get_test_name()
    print(' --------- Get TestName %s' % test_name)
    log_name = test_name + '.log'
    print("%s/../results/logs" % filepath)
    log_obj = Base_Logging(log_file_name=log_name, level=logging.DEBUG, filepath="%s/../results/logs" % filepath)
    return log_obj
