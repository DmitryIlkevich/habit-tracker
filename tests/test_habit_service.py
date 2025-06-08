import sqlite3
import pytest

from src.service.database_service import StorageService
from src.service.database_service import Database
from src.service.period_service import PeriodService
from src.service.habit_service import HabitService
from datetime import datetime


@pytest.fixture
def habit_service():
    connection = sqlite3.connect(":memory:")
    db = Database(connection=connection, ddl_file="../script/ddl.sql")
    storage_service = StorageService(db)
    period_service = PeriodService(storage_service)
    habit_service = HabitService(storage_service, period_service)
    yield habit_service


def test_get_habits(habit_service):
    assert len(habit_service.get_habits()) == 0
    habit_service.create_habit('Sport', 'Doing sport', 'Daily', '2025-05-01')
    assert len(habit_service.get_habits()) == 1


def test_create_habit(habit_service):
    habit_service.create_habit('Sport', 'Doing sport', 'Daily', '2025-05-01')
    habit_service.create_habit('Book reading', 'Read books', 'Weekly', '2024-02-15')

    habits = habit_service.get_habits()

    assert len(habits) == 2
    assert habits[0].name == 'Sport'
    assert habits[1].name == 'Book reading'


def test_get_habit_by_id(habit_service):
    habit_service.create_habit('Sport', 'Doing sport', 'Daily', '2025-05-01')
    habit_service.create_habit('Book reading', 'Read books', 'Weekly', '2024-02-15')
    result_habit = habit_service.get_habit_by_id(2)

    assert result_habit.name == 'Book reading'
    assert result_habit.period_type == 'Weekly'
    assert result_habit.description == 'Read books'
    assert len(result_habit.completed_periods) == 0
    assert result_habit.creation_date == '2024-02-15'


def test_get_habit_periods(habit_service):
    habit_service.create_habit('Sport', 'Doing sport', 'Daily', '2025-05-01')
    periods = habit_service.get_habit_periods(1)

    start_date = datetime.strptime('2025-05-01', '%Y-%m-%d')
    today = datetime.today()
    days_passed = (today - start_date).days + 1

    assert len(periods) == days_passed

    for period in periods:
        assert period.is_completed is False


def test_delete_habit(habit_service):
    habit_service.create_habit('Sport', 'Doing sport', 'Daily', '2025-05-01')
    habit_service.create_habit('Book reading', 'Read books', 'Weekly', '2024-02-15')

    habit_to_delete = habit_service.get_habit_by_id(1)
    habit_service.delete_habit(habit_to_delete)

    assert len(habit_service.get_habits()) == 1
    assert habit_service.get_habits()[0].name == 'Book reading'
