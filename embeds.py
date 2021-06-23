from datetime import timedelta, datetime


async def update_msg(new_message, msg):
    await msg.edit(content=new_message)


def new_msg():
    date_now = datetime.today()
    date_now_timestamp = int(date_now.timestamp())
    last_day_date = datetime(year=2021, month=6, day=25, hour=3, minute=0, second=0)
    last_day_timestamp = int(last_day_date.timestamp())
    remaining_time_seconds = last_day_timestamp - date_now_timestamp

    remaining_time = timedelta(seconds=remaining_time_seconds)
    remaining_days = remaining_time.days
    remaining_seconds = remaining_time.seconds

    remaining_minutes, remaining_seconds = divmod(remaining_seconds, 60)
    remaining_hours, remaining_minutes = divmod(remaining_minutes, 60)

    if remaining_days:
        if remaining_days > 1:
            remaining_days = '{} days '.format(remaining_days)
        else:
            remaining_days = '{} day '.format(remaining_days)
    else:
        remaining_days = ''

    if remaining_hours:
        if remaining_hours > 1:
            remaining_hours = '{} hours '.format(remaining_hours)
        else:
            remaining_hours = '{} hour '.format(remaining_hours)
    else:
        remaining_hours = ''

    if remaining_minutes:
        if remaining_minutes > 1:
            remaining_minutes = '{} minutes '.format(remaining_minutes)
        else:
            remaining_minutes = '{} minute '.format(remaining_minutes)
    else:
        remaining_minutes = ''

    if remaining_seconds:
        if remaining_seconds > 1:
            remaining_seconds = '{} seconds '.format(remaining_seconds)
        else:
            remaining_seconds = '{} second '.format(remaining_seconds)
    else:
        remaining_seconds = ''

    message = "{}{}{}{}".format(remaining_days, remaining_hours, remaining_minutes, remaining_seconds)
    return message
