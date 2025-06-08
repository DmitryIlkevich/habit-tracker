from src.service.habit_service import HabitService


class InsightsService:

    def __init__(self, habit_service: HabitService):
        """Gives analytical insights
        :param habit_service:
        """
        self.habit_service = habit_service

    def get_habits(self):
        """Retrieves all habits using habit service
        :return: habits
        """
        return self.habit_service.get_habits()

    def get_habits_by_type(self, habit_type):
        """Retrieves habits by type (day, week etc.)
        :param habit_type:
        :return: habits
        """
        return [habit for habit in self.get_habits() if habit.period_type == habit_type]

    def get_longest_streak_by_type(self, habit_type):
        """Retrieves longest streak by habit type (day, week)
        :param habit_type:
        :return: tuple habit with the longest periods list
        """
        result_habit = None
        result_periods = []

        for habit in self.get_habits_by_type(habit_type):
            streak = self.get_longest_streak_by_id(habit.habit_id)

            if len(streak) >= len(result_periods):
                result_habit = habit
                result_periods = streak

        return result_habit, result_periods

    def get_longest_run_streak(self):
        """Retrieves longest streak from all habit
        :return: tuple habit with the longest periods list
        """
        result_habit = None
        result_periods = []

        for habit in self.habit_service.get_habits():
            streak = self.get_longest_streak_by_id(habit.habit_id)

            if len(streak) >= len(result_periods):
                result_habit = habit
                result_periods = streak

        return result_habit, result_periods

    def get_longest_streak_by_id(self, habit_id):
        '''Retrieves longest streak from a specific habit
        :param habit_id:
        :return: longest streak by id
        '''
        max_periods = []
        curr_periods = []

        for period in self.habit_service.get_habit_periods(habit_id):
            if period.is_completed:
                curr_periods.append(period)
                if len(max_periods) <= len(curr_periods):
                    max_periods = curr_periods.copy()
            else:
                curr_periods.clear()

        return max_periods
