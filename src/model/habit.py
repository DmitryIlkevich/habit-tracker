class Habit:

    def __init__(self, habit_id, name, description, period_type, completed_periods, creation_date):
        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.period_type = period_type
        self.completed_periods = completed_periods
        self.creation_date = creation_date

    def __str__(self):
        res = f"{self.habit_id} {self.name} {self.description} {self.period_type}"
        periods_res = ' Periods ['
        for per in self.completed_periods:
            periods_res += str(per) + '; '
        periods_res += ']'
        return res + periods_res
