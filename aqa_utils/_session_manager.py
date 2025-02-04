import os
import allure
import pytest

from aqa_utils.log_util import get_log_memo, log


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport():
    outcome = yield
    result = outcome.get_result()
    if result.failed:
        if result.when == 'setup':
            try:
                allure.attach(
                    body=get_log_memo().get_logs(),
                    name='Setup Logs',
                    attachment_type=allure.attachment_type.HTML,
                )
            except Exception as e:
                log.error(f'Failed to attach setup logs: {str(e)}')
        if result.when == 'call':
            try:
                allure.attach(
                    body=get_log_memo().get_logs(),
                    name='Test Logs',
                    attachment_type=allure.attachment_type.HTML,
                )
            except Exception as e:
                log.error(f'Failed to attach test logs: {str(e)}')
        if result.when == 'teardown':
            try:
                allure.attach(
                    body=get_log_memo().get_logs(),
                    name='Teardown Logs',
                    attachment_type=allure.attachment_type.HTML,
                )
            except Exception as e:
                log.error(f'Failed to attach teardown logs: {str(e)}')

    get_log_memo().clear_logs()


def pytest_addoption(parser):
    parser.addini("alluredir", "Directory to store Allure results", default="./allure_results")
    parser.addini("clean_alluredir", "Clean Allure results directory before running tests", default=True)
    parser.addini("allure_no_capture", "Disable stdout/stderr capturing", default=True)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    allure_results_dir = os.path.join(config.rootdir, 'allure_results')
    config.option.allure_report_dir = allure_results_dir

    clean_alluredir = config.getoption("--clean-alluredir", default=config.getini("clean_alluredir"))
    config.option.clean_alluredir = clean_alluredir

    allure_no_capture = config.getoption("--allure-no-capture", default=config.getini("allure_no_capture"))
    config.option.allure_no_capture = allure_no_capture

    addopts = config.getoption('addopts', '').split()
    if clean_alluredir and "--clean-alluredir" not in addopts:
        addopts.append("--clean-alluredir")
    if allure_no_capture and "--allure-no-capture" not in addopts:
        addopts.append("--allure-no-capture")

    config.option.addopts = ' '.join(addopts)


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args):
    if "--clean-alluredir" not in args:
        args.append("--clean-alluredir")
    if "--allure-no-capture" not in args:
        args.append("--allure-no-capture")
