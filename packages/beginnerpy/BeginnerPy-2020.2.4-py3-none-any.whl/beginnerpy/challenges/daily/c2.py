from datetime import date

from calendar import monthrange
import datetime


def has_friday_13(month, yr):
    yr -= month < 3
    month_values = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    return (
        False
        if (yr + yr // 4 - yr // 100 + yr // 400 + month_values[month - 1] + 13) % 7
        != 5
        else True
    )


for y in range(1, 10000):
    for m in range(12):
        assert has_friday_13(m + 1, y) == (date(y, m + 1, 13).weekday() == 4)
print("Success")
