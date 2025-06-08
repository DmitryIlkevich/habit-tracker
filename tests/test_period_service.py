import sqlite3
import pytest

from src.model import Habit
from src.service.database_service import StorageService
from src.service.database_service import Database
from src.service.period_service import PeriodService
from datetime import datetime


@pytest.fixture
def period_service():
    connection = sqlite3.connect(":memory:")
    db = Database(connection=connection, ddl_file="../script/ddl.sql")
    storage_service = StorageService(db)
    period_service = PeriodService(storage_service)
    yield period_service


def test_add_period(period_service):
    period_service.add_period(10, '2025-01-01', '2025-01-30')

    periods = period_service.get_completed_periods_by_habit_id(10)

    assert len(periods) == 1
    period = periods[0]
    assert period.habit_id == 10
    assert period.start_date == '2025-01-01'
    assert period.end_date == '2025-01-30'


def test_get_completed_periods_by_habit_id(period_service):
    period_service.add_period(10, '2025-01-01', '2025-01-10')
    period_service.add_period(11, '2025-02-01', '2025-03-20')
    period_service.add_period(11, '2025-01-01', '2025-01-30')

    periods1 = period_service.get_completed_periods_by_habit_id(10)
    periods2 = period_service.get_completed_periods_by_habit_id(11)

    assert len(periods1) == 1
    assert len(periods2) == 2


def test_delete_period(period_service):
    period_service.add_period(10, '2025-01-01', '2025-01-10')
    period_service.add_period(10, '2025-02-01', '2025-03-20')
    period_service.delete_period(1)

    period = period_service.get_completed_periods_by_habit_id(10)[0]
    assert period.period_id == 2
    assert period.start_date == '2025-02-01'


def test_get_period_start_date_daily_type(period_service):
    result = period_service.get_period_start_date('2025-01-01', 'Daily')
    expected = datetime.strptime('2025-01-01', "%Y-%m-%d").date()
    assert expected == result


def test_get_all_periods(period_service):
    period_service.add_period(10, '2025-01-01', '2025-01-01')
    period_service.add_period(10, '2025-01-02', '2025-01-02')
    period_service.add_period(10, '2025-01-10', '2025-01-10')
    completed_periods = period_service.get_completed_periods_by_habit_id(10)
    habit = Habit(1, "Sport", "Doing sport", 'Daily', completed_periods, '2025-01-01')

    start_date = datetime.strptime('2025-01-01', '%Y-%m-%d')
    today = datetime.today()
    days_passed = (today - start_date).days + 1

    result_periods = period_service.get_all_periods(habit)

    assert days_passed == len(result_periods)
    assert result_periods[0].is_completed is True
    assert result_periods[1].is_completed is True
    assert result_periods[2].is_completed is False
    assert result_periods[9].is_completed is True
