import datetime
import random
import pytz


class DateTimeUtil:
    @staticmethod
    def get_zone_id(zone_locale: str) -> datetime.tzinfo:
        try:
            return pytz.timezone(zone_locale)
        except pytz.UnknownTimeZoneError:
            raise ValueError(f'Time zone invalid: {zone_locale}')

    @staticmethod
    def get_now_datetime(pattern: str) -> str:
        return datetime.datetime.now().strftime(pattern)

    @staticmethod
    def get_now_timestamp() -> float:
        return datetime.datetime.now().timestamp()

    @staticmethod
    def get_random_date_of_pattern(pattern: str, start_year: int = 20, end_year: int = 70) -> str:
        today = datetime.date.today()
        random_days = random.randint(365 * start_year, 365 * end_year)
        random_date = today - datetime.timedelta(days=random_days)
        return random_date.strftime(pattern)
