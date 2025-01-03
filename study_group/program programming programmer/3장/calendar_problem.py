

DAYS_PER_MONTH = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def check_number_of_days_given_month_day(month1, day1, month2, day2):
    assert(month1 <= month2) # 편의상 이런 제한조건 건다.

    if month1 < month2:
        current_month_remaining_day = DAYS_PER_MONTH[month1]-day1
    else:
        return day2 - day1
    further_month_remaining_day = day2

    total_intermediate_days = 0
    for i in range(month1+1, month2):
        total_intermediate_days += DAYS_PER_MONTH[i]

    return current_month_remaining_day + total_intermediate_days + further_month_remaining_day

def check_week_day_given_month_day(month, day):
    """ 무슨 요일인지 - 1월 1일이 월요일인 셈 치자"""

    days = check_number_of_days_given_month_day(1, 1, month, day)
    weekday_index = days % 7
    return weekday_index

# def print_year_and_month_calendar(year, month):
    # 1년 1월 1일이 월요일,
    # check_week_day_given_month_day를 불러서 특정 달의 첫 날짜의 요일을 알고, 쭈르르 쓰면된다.


if __name__ == '__main__':
    days = check_number_of_days_given_month_day(1,1, 2,1) # 31일
    days2 = check_number_of_days_given_month_day(1,5, 2,1) #
    days3 = check_number_of_days_given_month_day(1,5, 3,1) #

    weekday = check_week_day_given_month_day(1,2) # 1은 화요일
