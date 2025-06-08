import sqlite3
import pytest

from src.service.database_service import StorageService
from src.service.database_service import Database
from src.service.period_service import PeriodService
from src.service.habit_service import HabitService
from src.service.insights_service import InsightsService


@pytest.fixture
def services():
    connection = sqlite3.connect(":memory:")
    db = Database(connection=connection, ddl_file="../script/ddl.sql")
    storage_service = StorageService(db)
    period_service = PeriodService(storage_service)
    habit_service = HabitService(storage_service, period_service)
    insights_service = InsightsService(habit_service)
    yield (insights_service, habit_service, period_service)


def test_get_habits(services):
    insights_service, habit_service, period_service = services
    assert len(insights_service.get_habits()) == 0
    habit_service.create_habit('Sport', 'Doing sport', 'Daily', '2025-05-01')
    assert len(insights_service.get_habits()) == 1


def test_get_daily_habits(services):
    insights_service, habit_service, period_service = services
    habit_service.create_habit('Sport', 'Doing sport', 'Daily', '2025-05-01')
    habit_service.create_habit('Film', 'Film watching', 'Daily', '2025-04-01')
    habit_service.create_habit('Book reading', 'Read books', 'Weekly', '2024-02-15')
    daily_habits = insights_service.get_habits_by_type('Daily')

    assert len(daily_habits) == 2
    assert daily_habits[0].name == 'Sport'
    assert daily_habits[1].name == 'Film'


def test_get_weekly_habits(services):
    insights_service, habit_service, period_service = services
    habit_service.create_habit('Sport', 'Doing sport', 'Daily', '2025-05-01')
    habit_service.create_habit('Film', 'Film watching', 'Daily', '2025-04-01')
    habit_service.create_habit('Book reading', 'Read books', 'Weekly', '2024-02-15')
    daily_habits = insights_service.get_habits_by_type('Weekly')

    assert len(daily_habits) == 1
    assert daily_habits[0].name == 'Book reading'


def test_get_longest_streak_by_type(services):
    insights_service, habit_service, period_service = services
    habit_service.create_habit('Sport1', 'Doing sport', 'Daily', '2025-05-01')
    habit_service.create_habit('Sport2', 'Doing sport', 'Daily', '2025-04-02')

    period_service.add_period(1, '2025-05-03', '2025-05-03')
    period_service.add_period(1, '2025-05-04', '2025-05-04')
    period_service.add_period(2, '2025-05-05', '2025-05-05')

    habit, periods = insights_service.get_longest_streak_by_type('Weekly')
    assert habit is None

    habit, periods = insights_service.get_longest_streak_by_type('Daily')
    assert habit.habit_id == 1
    assert len(periods) == 2
    assert periods[0].start_date == '2025-05-03'
    assert periods[1].start_date == '2025-05-04'


def test_get_longest_run_streak(services):
    insights_service, habit_service, period_service = services
    habit_service.create_habit('Sport1', 'Doing sport', 'Daily', '2025-05-01')
    habit_service.create_habit('Sport2', 'Doing sport', 'Daily', '2025-04-02')

    period_service.add_period(1, '2025-05-03', '2025-05-03')
    period_service.add_period(1, '2025-05-04', '2025-05-04')
    period_service.add_period(2, '2025-05-05', '2025-05-05')

    habit, periods = insights_service.get_longest_run_streak()
    assert habit.habit_id == 1
    assert len(periods) == 2
    assert periods[0].start_date == '2025-05-03'
    assert periods[1].start_date == '2025-05-04'


def test_get_longest_streak_by_id(services):
    insights_service, habit_service, period_service = services
    habit_service.create_habit('Sport1', 'Doing sport', 'Daily', '2025-05-01')
    habit_service.create_habit('Sport2', 'Doing sport', 'Daily', '2025-04-02')

    period_service.add_period(1, '2025-05-03', '2025-05-03')
    period_service.add_period(1, '2025-05-04', '2025-05-04')
    period_service.add_period(2, '2025-05-05', '2025-05-05')

    periods = insights_service.get_longest_streak_by_id(2)
    assert len(periods) == 1
    assert periods[0].start_date == '2025-05-05'

