from aqa_utils.log_util import log


def fail(message):
    """Fail execution intentionally"""
    assert False, message


class Assert:

    @staticmethod
    def that_dicts_same(actual, expected, message):
        missing_pairs = [
            f'{key} -> {expected[key]}'
            for key in expected
            if key not in actual or actual[key] != expected[key]
        ]

        unexpected_pairs = [
            f'{key} -> {actual[key]}'
            for key in actual
            if key not in expected or actual[key] != expected[key]
        ]

        if missing_pairs or unexpected_pairs:
            error_builder = [message]
            if missing_pairs:
                error_builder.append('\nExpected:')
            error_builder.extend(f'\n{pair}' for pair in missing_pairs)
            if unexpected_pairs:
                error_builder.append('\nActual:')
            error_builder.extend(f'\n{pair}' for pair in unexpected_pairs)
            error = "".join(error_builder)
            raise AssertionError(error)

    @staticmethod
    def that_true(condition, message):
        assert condition, message

    @staticmethod
    def that_false(condition, message):
        assert not condition, message

    @staticmethod
    def that_same(actual, expected, message):
        log.debug(f'Assert equality : {expected} <-> {actual}')
        assert actual == expected, f'{message} - Expected: {expected}, Actual: {actual}'

    @staticmethod
    def that_not_same(actual, expected, message):
        log.debug(f'Assert inequality : {expected} <-> {actual}')
        assert actual != expected, f"{message} - Expected not to be: '{expected}', Actual: '{actual}'"

    @staticmethod
    def that_contains(actual, expected, message):
        log.debug(f'Assert contains : {expected} <-> {actual}')
        assert expected in actual, f"{message} - Expected '{expected}' to be contained in '{actual}'"

    @staticmethod
    def that_not_contains(actual, expected, message):
        log.debug(f'Assert not contains : {expected} <-> {actual}')
        assert expected not in actual, f"{message} - Expected '{expected}' not to be contained in '{actual}'"
