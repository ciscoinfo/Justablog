import datetime as dt


def get_date():
    date_today = dt.date.today().strftime("%B %d, %Y")
    return date_today