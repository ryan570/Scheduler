from datetime import datetime
import calendar

calendarObject = calendar.Calendar(firstweekday=6)

def createCalendar():
    currentYear = datetime.now().year
    currentMonth = datetime.now().month
    month = calendarObject.monthdayscalendar(currentYear, currentMonth)
    updatedMonth = [[" " if x==0 else x for x in line] for line in month]
    return updatedMonth

def customMonth(monthNumber, year):
    month = calendarObject.monthdayscalendar(year, monthNumber)
    updatedMonth = [[" " if x==0 else x for x in line] for line in month]
    return updatedMonth

def monthString(monthNumber):
    monthName = calendar.month_name[monthNumber]
    return monthName