import sqlite3

from src.model import Habit, Period


class Database:

    def __init__(self, db_name=None, ddl_file=None, connection=None):
        """Stores database connection and init database
        :param db_name:
        :param ddl_file:
        :param connection:
        """
        self.connection = connection or sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        if ddl_file:
            with open(ddl_file, "r") as file:
                ddl_script = file.read()
                self.cursor.executescript(ddl_script)
                self.connection.commit()


class StorageService:

    def __init__(self, database):
        """Layer for interaction with database
        :param database: connection to DB
        """
        self.database = database

    def create_habit(self, name, description, period_type, creation_date):
        """Creates habit
        :param name:
        :param description:
        :param period_type:
        :param creation_date:
        """
        query = f"""
        INSERT INTO habit (
            name,
            description,
            period_type,
            creation_date)
        VALUES (?, ?, ?, ?);
        """
        self.database.cursor.execute(query, (name, description, period_type, creation_date))
        self.database.connection.commit()

    def get_habits(self):
        """ Get all habits from database
        :return: Habits
        """
        query = f"""
        SELECT id, name, description, period_type, creation_date
        FROM habit;
        """

        rows = self.database.cursor.execute(query).fetchall()
        result = []
        for row in rows:
            habit_id, name, description, period_type, creation_date = row
            completed_periods = self.get_periods_by_habit_id(habit_id)
            habit = Habit(habit_id, name, description, period_type, completed_periods, creation_date)
            result.append(habit)

        return result

    def get_habit_by_id(self, habit_id):
        """Retrieve habit from database by id
        :param habit_id:
        :return: habit if present
        """
        query = f"""
        SELECT id, name, description, period_type, creation_date
        FROM habit
        WHERE id = ?
        """

        self.database.cursor.execute(query, (habit_id,))
        row = self.database.cursor.fetchone()

        habit_id, name, description, period_type, creation_date = row
        completed_periods = self.get_periods_by_habit_id(habit_id)
        return Habit(habit_id, name, description, period_type, completed_periods, creation_date)

    def delete_habit(self, habit_id):
        """Deletes habit from database by id
        :param habit_id:
        """
        query = f"""
        DELETE FROM habit
        WHERE id = ?
        """

        self.database.cursor.execute(query, (habit_id,))
        self.database.connection.commit()

    def create_period(self, habit_id, start_date, end_date):
        """Creates period for a specific habit with start and end date
        :param habit_id:
        :param start_date: period start date
        :param end_date: period end date
        """
        query = f"""
        INSERT INTO completed_period (
            habit_id,
            start_date,
            end_date)
        VALUES (?, ?, ?)
        """
        self.database.cursor.execute(query, (habit_id, start_date, end_date))
        self.database.connection.commit()

    def get_periods_by_habit_id(self, habit_id):
        """Retrieves habit from database by id
        :param habit_id:
        :return: habit
        """
        query = f"""
        SELECT id, habit_id, start_date, end_date, is_completed
        FROM completed_period
        WHERE habit_id = ?
        """

        result = []
        for row in self.database.cursor.execute(query, (habit_id,)):
            period_id, habit_id, start_date, end_date, is_completed = row
            result.append(Period(habit_id, start_date, end_date, period_id, is_completed))
        return result

    def delete_period(self, period_id):
        """Deleted period from database by period id
        :param period_id:
        """
        query = f"""
        DELETE FROM completed_period
        WHERE id = ?
        """

        self.database.cursor.execute(query, (period_id,))
        self.database.connection.commit()
