from aqa_ui.selen.driver.driver_mode.local_driver import LocalDriver
from aqa_ui.selen.driver.driver_mode.remote_driver import RemoteDriver


class Driver:

    @staticmethod
    def create_instance(remote: bool, hub: str, browser: str, headless: bool):
        if remote:
            return RemoteDriver().provide_instance(browser, hub)
        else:
            return LocalDriver().provide_instance(browser, headless)
