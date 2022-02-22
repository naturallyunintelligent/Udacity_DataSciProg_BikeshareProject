import time
import datetime
import pandas as pd
import numpy as np

# Useful reference notes:
# https://realpython.com/python-datetime/
# https://www.kite.com/python/answers/how-to-convert-between-month-name-and-month-number-in-python
# https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
# regex:
# https://stackoverflow.com/questions/43281715/regex-that-matches-all-week-days-name-in-a-string
# https://pythex.org/


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def greeting() -> str :
    """
    Checks local time and returns a suitable greeting
    :return greeting_time: an appropriate greeting for the local time
    """
    if time.localtime().tm_hour < 12:
        greeting_time = "Good morning"
    elif time.localtime().tm_hour  < 18:
        greeting_time = "Good afternoon"
    else:
        greeting_time = "Good evening"
    return greeting_time

def get_city() -> str:
    """
    Takes input from the user to choose a city to analyse
    :return city: the city chosen for analysis
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('\nWhich city would you like to analyse? '
                             'Data available for Chicago, New York City and Washington\n'))
            city = city.lower()
            if city not in ['chicago', 'new york city', 'washington']:
                print("Apologies, I didn't understand that, please enter Chicago, New York City or Washington")
                continue
        except ValueError:
            print("Apologies, I didn't understand that, please enter Chicago, New York City or Washington")
            continue
        else:
            break
    return city

def get_month() -> int:
    """
    Takes input from the user to choose a month to analyse
    :return month_number: an integer to represent the calendar month
    """
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            chosen_month = input('\nWhich month would you like to analyse?\n').lower()
            if type(chosen_month) != str:
                print(
                    'TypeError: Apologies, only strings handled, please enter a calendar month in English, e.g. January, '
                    'February, March, April, May, June, July, September, October, November or December')
                continue
            if chosen_month in [
                'january',
                'february',
                'march',
                'april',
                'may',
                'june',
                'july',
                'august',
                'september',
                'october',
                'december', ]:
                chosen_month = datetime.datetime.strptime(chosen_month, "%B")
                chosen_month = chosen_month.strftime("%b")
            if chosen_month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'dec', ]:
                chosen_month = datetime.datetime.strptime(chosen_month, "%b")
                month_number = chosen_month.month
                print(month_number)
                break
            if chosen_month not in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'dec', ]:
                print(
                    "Apologies, I didn't understand that please enter a calendar month in English, e.g. January, "
                    "February, March, April, May, June, July, September, October, November or December")
                continue
        except TypeError:
            print('TypeError: Apologies, numbers not handled, please enter a calendar month in English, e.g. January, '
                  'February, March, April, May, June, July, September, October, November or December')
            continue
        except ValueError:
            print('ValueError: Please enter a calendar month in English, e.g. January, '
                  'February, March, April, May, June, July, September, October, November or December')
            continue
        except KeyboardInterrupt:
            print("Keyboard Interrupt - no input taken")
            break
        finally:
            print("Attempted input")

    return month_number

def get_day() -> int:
    """
    Takes input from the user to choose a day to analyse
    :return day_number: an integer to represent the day of the week
    """
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day_name = str(input('\nWhich day would you like to analyse?\n')).lower()
        except:
            print('Please enter a day of the week in English, e.g. Monday, '
                  'Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday')
            continue
        else:
            break

    if day_name in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',]:
        chosen_day = datetime.datetime.strptime(day_name, "%a")
    elif day_name in [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday', ]:
        chosen_day = datetime.datetime.strptime(day_name, "%A")

    day_number = chosen_day.day
    print(day_number)
    return day_number

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    city = get_city()
    month = get_month()
    day = get_day()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    #df =
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    # useful month conversion:
    # month_number = "3"
    # datetime_object = datetime.datetime.strptime(month_number, "%m")
    # month_name = datetime_object.strftime("%b")
    # print(month_name)
    # OUTPUT
    # Mar
    #
    # full_month_name = datetime_object.strftime("%B")
    # print(full_month_name)






    # display the most common day of week


    # display the most common start hour


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station


    # display most commonly used end station


    # display most frequent combination of start station and end station trip


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time


    # display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types


    # Display counts of gender


    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    greeting_for_now = greeting()
    print(f'{greeting_for_now}! Let\'s explore some US bikeshare data!')
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
