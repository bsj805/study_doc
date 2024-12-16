def days_between_dates(y1, m1, d1, y2, m2, d2):
    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def days_in_month(year, month):
        days = [31, 28 + is_leap_year(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return days[month - 1]

    def date_to_days(year, month, day):
        days = 0
        for y in range(1, year):
            days += 365 + is_leap_year(y)
        for m in range(1, month):
            days += days_in_month(year, m)
        days += day
        return days

    days1 = date_to_days(y1, m1, d1)
    days2 = date_to_days(y2, m2, d2)
    return abs(days2 - days1)

def day_of_week(year, month, day):
    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def days_in_month(year, month):
        days = [31, 28 + is_leap_year(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return days[month - 1]

    # Reference date: 1 Jan 0001 is a Monday (day 1)
    days = day
    for y in range(1, year):
        days += 365 + is_leap_year(y)
    for m in range(1, month):
        days += days_in_month(year, m)

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return weekdays[(days - 1) % 7]

def generate_calendar(year, month):
    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def days_in_month(year, month):
        days = [31, 28 + is_leap_year(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return days[month - 1]

    def day_of_week(year, month, day):
        days = day
        for y in range(1, year):
            days += 365 + is_leap_year(y)
        for m in range(1, month):
            days += days_in_month(year, m)
        return (days - 1) % 7  # 0 = Monday, 6 = Sunday

    days = days_in_month(year, month)
    start_day = day_of_week(year, month, 1)  # Day of the week for 1st day of the month

    calendar = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    calendar_grid = calendar + [""] * start_day + [str(i) for i in range(1, days + 1)]

    # Arrange into weeks (rows of 7)
    rows = []
    for i in range(0, len(calendar_grid), 7):
        rows.append(calendar_grid[i:i + 7])

    # Format the result as strings
    return [" ".join(row).strip() for row in rows]