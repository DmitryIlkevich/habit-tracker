from datetime import datetime

from src.service.database_service import StorageService
from src.service.period_service import PeriodService


class HabitService:

    def __init__(self, storage_service: StorageService, period_service: PeriodService):
        """Responsible for habit object manipulation
        :param storage_service: Storage service
        :param period_service: Period service
        """
        self.storage_service = storage_service
        self.period_serive = period_service

    def create_habit(self, name, description, period_type, period_start=datetime.now().strftime("%Y-%m-%d")):
        """Creates new habit by querying database layer
        :param name: Habit name
        :param description: Habit description
        :param period_type: Period type (day, week etc.)
        :param period_start: Period start date
        :return: Void
        """
        self.storage_service.create_habit(name, description, period_type, period_start)

    def get_habits(self):
        """Retrieves all habits from database
        :return: Habits
        """
        return self.storage_service.get_habits()

    def get_habit_by_id(self, habit_id):
        """Retrieves habit by habit id
        :param habit_id:
        :return: Habit or None
        """
        return self.storage_service.get_habit_by_id(habit_id)

    def get_habit_periods(self, habit_id):
        """Retrieves habit and uses period service to retrieve periods
        :param habit_id:
        :return: Habit periods
        """
        habit = self.storage_service.get_habit_by_id(habit_id)
        return self.period_serive.get_all_periods(habit)

    def delete_habit(self, habit):
        """Removes habit from database
        :param habit: Habit object
        """
        periods = self.period_serive.get_all_periods(habit)

        for period in periods:
            self.period_serive.delete_period(period.period_id)

        self.storage_service.delete_habit(habit.habit_id)