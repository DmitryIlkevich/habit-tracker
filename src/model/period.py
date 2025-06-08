from abc import ABC, abstractmethod


class Period:
    '''Domain business object for Periods'''
    def __init__(self, habit_id, start_date, end_date, period_id=None, is_completed=False):
        self.period_id = period_id
        self.habit_id = habit_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_completed = bool(is_completed)

    def __str__(self):
        return f"period_id: {self.period_id} habit_id: {self.habit_id} {self.start_date} {self.end_date} {self.is_completed}"


