from aqa_utils.log_util import log

import time


class RetryUtil:
    @staticmethod
    def retry(num_repeats: int, executor, log_on_fail: str, delay: int = 3):
        retries_left = num_repeats
        while retries_left > 0:
            try:
                executor()
                return
            except Exception as e:
                retries_left -= 1
                log.debug(f"Exception caught during retry attempt: {e}")
                time.sleep(delay)
        raise ValueError(log_on_fail)

    @staticmethod
    def repeat(num_repeats: int, executor, log_on_fail: str, delay: int = 3):
        for _ in range(num_repeats):
            RetryUtil.retry(1, executor, log_on_fail, delay)
