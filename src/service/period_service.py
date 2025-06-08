from datetime import datetime, timedelta

from src.model import Period


class PeriodService:

    def __init__(self, storage_service):
        """Responsible for handling period data
        :param storage_service:
        """
        self.storage_service = storage_service

    def add_period(self, habit_id, start_period_date, end_period_date):
        """Create new period
        :param habit_id:
        :param start_period_date:
        :param end_period_date:
        """
        self.storage_service.create_period(habit_id, start_period_date, end_period_date)

    def get_completed_periods_by_habit_id(self, habit_id):
        '''Retrieves completed periods from database
        :param habit_id:
        :return: completed periods
        '''
        return self.storage_service.get_periods_by_habit_id(habit_id)

    def delete_period(self, period_id):
        """Removes period from database
        :param period_id:
        """
        self.storage_service.delete_period(period_id)

    def get_period_start_date(self, habit_start_date, period_type):
        """Calculates first possible period start date using habit start date
        :param habit_start_date:
        :param period_type:
        :return:
        """
        date = datetime.strptime(habit_start_date, "%Y-%m-%d").date()
        if period_type == 'Weekly':
            date = date - timedelta(days=(date.weekday()))

        return date

    def get_all_periods(self, habit):
        """Retrieves completed periods form database. Calculates not completed periods.
        :param habit:
        :return: completed and non-completed periods
        """
        step = 7 if habit.period_type == 'Weekly' else 1
        sorted_periods = sorted(habit.completed_periods, key=lambda p: p.start_date)
        start_date = self.get_period_start_date(habit.creation_date, habit.period_type)
        now_date = datetime.now().date()

        result_periods = []

        while start_date <= now_date:
            if len(sorted_periods) > 0:
                if get_date(sorted_periods[0].start_date) > start_date:
                    result_periods.append(Period(habit.habit_id, start_date, start_date + timedelta(days=step - 1)))
                    start_date = start_date + timedelta(days=step)
                elif get_date(sorted_periods[0].start_date) == start_date:
                    result_periods.append(sorted_periods.pop(0))
                    start_date = start_date + timedelta(days=step)
            else:
                result_periods.append(Period(habit.habit_id, start_date, start_date + timedelta(days=step - 1)))
                start_date = start_date + timedelta(days=step)

        return result_periods


def get_date(date):
    return datetime.strptime(date, "%Y-%m-%d").date()
