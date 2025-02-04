from random import randint


class IntegerUtil:

    @staticmethod
    def get_random_integer(min_val: int = 3, max_val: int = 10) -> int:
        return randint(min_val, max_val)

    @staticmethod
    def get_first_int_or_default(default: int, *arr) -> int:
        for i in arr:
            if i != 0:
                return i
        return default
