import datetime
import calendar


def get_birthdays_per_week(users):

    currentWeek, holidays = current_week()

    for nm, dt in users.items():
        date1 = dt.replace(f'{dt[:4]}', '2022')
        if date1 in currentWeek:
            day = week_day(date1)
            print(f'{day}: {nm}')
        elif date1 in holidays:
            day = week_day(date1)
            print(f'Monday: {nm}')


def current_week():

    week_day = datetime.datetime.now().isocalendar()[2]
    start_date = datetime.datetime.now() - datetime.timedelta(days=week_day - 1)
    next_mon = next_weekday(start_date, 0)
    dates = [str((next_mon + datetime.timedelta(days=i)).date()) for i in range(7)]
    holidays = [str((next_mon - datetime.timedelta(days=i)).date()) for i in range(1, 3)]
    return dates, holidays


def week_day(user_date):

    year, month, day = user_date.split('-')
    idx_day = datetime.datetime(int(year), int(month), int(day)).weekday()
    return calendar.day_name[idx_day]


def next_weekday(d, weekday):
    
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


weekdays = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
users = dict(Bill='1993-02-13', Luk='2001-02-14', Jamse='1995-02-15', Tim='1998-02-20', Andrew='1977-02-14')
get_birthdays_per_week(users)
