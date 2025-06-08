import click
from InquirerPy import inquirer

from src.service.database_service import StorageService
from src.service.database_service import Database
from src.service.period_service import PeriodService
from src.service.insights_service import InsightsService
from src.service.habit_service import HabitService

db = Database(db_name="script/habit-tracker.db", ddl_file="script/ddl.sql")
storage_service = StorageService(db)
period_service = PeriodService(storage_service)
habit_service = HabitService(storage_service, period_service)
insights_service = InsightsService(habit_service)


@click.command()
def menu():
    '''
    Represent menu method which allows to communicate with user by CLI
    '''
    while True:
        action = inquirer.select(
            message="",
            border=True,
            qmark="",
            choices=[
                "List habits",
                "Create habit",
                "Insights",
                "Exit"
            ],
        ).execute()

        if action == "List habits":
            list_habits()
        elif action == "Create habit":
            create_habit()
        elif action == "Exit":
            click.echo("See you soon")
            break
        elif action == "Insights":
            get_insights()


def get_insights():
    action = inquirer.select(
        message="",
        border=True,
        qmark="",
        choices=[
            "All currently tracked habits",
            "All daily habits",
            "All weekly habits",
            "Longest run streak",
            "Longest run streak for daily habit",
            "Longest run streak for weekly habit",
            "<= Return"
        ],
    ).execute()

    if action == "All currently tracked habits":
        habits = insights_service.get_habits()
        print_habits(habits)
        get_insights()
    elif action == "All daily habits":
        habits = insights_service.get_habits_by_type("Daily")
        print_habits(habits)
        get_insights()
    elif action == "All weekly habits":
        habits = insights_service.get_habits_by_type("Weekly")
        print_habits(habits)
        get_insights()
    elif action == "Longest run streak":
        habit, periods = insights_service.get_longest_run_streak()
        if habit is None:
            click.echo("No streaks at all")
        else:
            print_habits([habit])
            print_periods(periods)
    elif action == "Longest run streak for daily habit":
        habit, periods = insights_service.get_longest_streak_by_type("Daily")
        if habit is None:
            click.echo("No streaks at all")
        else:
            print_habits([habit])
            print_periods(periods)
    elif action == "Longest run streak for weekly habit":
        habit, periods = insights_service.get_longest_streak_by_type("Weekly")
        if habit is None:
            click.echo("No streaks at all")
        else:
            print_habits([habit])
            print_periods(periods)
    elif action == "<= Return":
        return


def create_habit():
    name = inquirer.text(message="Habit name:").execute()
    description = inquirer.text(message="Description:").execute()
    period_start = inquirer.text(message="Period start <yyyy-MM-dd>:").execute()
    period_type = inquirer.select(
        message="Period:",
        choices=["Daily", "Weekly"]
    ).execute()

    click.echo(period_type)
    habit_service.create_habit(name, description, period_type, period_start)
    click.echo(f"Habit '{name}' added!")


def list_habits():
    habits = habit_service.get_habits()

    if not habits:
        click.echo("No habits found!")
        return

    habit_names = []
    for habit in habits:
        habit_names.append(habit.name)
    habit_names.append("<= Return")

    result = inquirer.select(
        border=True,
        qmark="",
        message="Chose for details",
        choices=habit_names,
    ).execute()

    if result == "<= Return":
        return
    else:
        for habit in habits:
            if habit.name == result:
                show_habit_menu(habit.habit_id)


def period_details(period, habit_id):
    click.echo(
        click.style(f"{period.start_date}-{period.end_date} Completed: {period.is_completed}",
                    fg="green",
                    bold=True))

    choices = []
    if period.is_completed:
        choices.append("Mark as not complete")
    else:
        choices.append("Mark as complete")
    choices.append("<= Return")

    result = inquirer.select(
        border=True,
        qmark="",
        message="Options",
        choices=choices,
    ).execute()

    if result == "<= Return":
        show_habit_menu(habit_id)
    elif result == "Mark as complete":
        period_service.add_period(period.habit_id, str(period.start_date), str(period.end_date))
        period.is_completed = True
        period_details(period, habit_id)
    elif result == "Mark as not complete":
        period_service.delete_period(period.period_id)
        period.is_completed = False
        period_details(period, habit_id)


def show_habit_menu(habit_id):
    result = inquirer.select(
        border=True,
        qmark="",
        message="Chose action",
        choices=[
            "Details",
            "Periods",
            "Longest run streak",
            "Delete",
            "<= Return"
        ],
    ).execute()

    if result == "Details":
        habit = habit_service.get_habit_by_id(habit_id)
        click.echo(
            click.style(f"Name: {habit.name}\n"
                        f"Period type: {habit.period_type}\n"
                        f"Description: {habit.description}\n"
                        f"Creation date: {habit.creation_date}",
                        fg="green",
                        bold=True))
        result = inquirer.select(
            border=True,
            qmark="",
            message="Options",
            choices=[
                "<= Return"
            ],
        ).execute()

        if result == "<= Return":
            show_habit_menu(habit_id)
    elif result == "Periods":
        periods = habit_service.get_habit_periods(habit_id)

        period_names_to_periods = dict()
        for period in periods:
            period_name = f"{period.start_date}-{period.end_date} Completed: {period.is_completed}"
            period_names_to_periods[period_name] = period

        period_names_to_periods["<= Return"] = ""

        result = inquirer.select(
            border=True,
            qmark="",
            message="Options",
            choices=list(period_names_to_periods.keys()),
        ).execute()

        if result == "<= Return":
            show_habit_menu(habit_id)
        else:
            for k, v in period_names_to_periods.items():
                if k == result:
                    period_details(v, habit_id)
                    break

    elif result == "Delete":
        habit_service.delete_habit(habit_service.get_habit_by_id(habit_id))
        list_habits()
    elif result == "Longest run streak":
        longest_streak = insights_service.get_longest_streak_by_id(habit_id)
        habit = habit_service.get_habit_by_id(habit_id)
        click.echo(
            click.style(f"Name: {habit.name}\n"
                        f"Period type: {habit.period_type}\n"
                        f"Description: {habit.description}\n"
                        f"Creation date: {habit.creation_date}", fg="green",
                        bold=True))

        if len(longest_streak) > 0:
            click.echo("Longest run streak:")
            for period in longest_streak:
                click.echo(
                    click.style(f"{period.start_date} - {period.end_date}",
                                fg="blue",
                                bold=True))
        else:
            click.echo(click.style(f"No completed periods found"))

        show_habit_menu(habit_id)


def print_habits(habits):
    for habit in habits:
        click.echo(click.style(f"{habit.name}",
                               fg="green",
                               bold=True))


def print_periods(periods):
    for period in periods:
        click.echo(click.style(f"{period.start_date} - {period.end_date}",
                                          fg="blue",
                                          bold=False))


if __name__ == '__main__':
    menu()
