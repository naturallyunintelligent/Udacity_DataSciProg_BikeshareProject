import time
import parse
import datetime
import pandas as pd
import numpy as np


# TODO: regex in user inputs
# TODO: remove whitespace in user inputs

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def greeting() -> None:
    """
    Checks local time and prints a suitable greeting
    :return: None
    """

    if time.localtime().tm_hour < 12:
        greeting_for_now = "Good morning"
    elif time.localtime().tm_hour  < 18:
        greeting_for_now = "Good afternoon"
    else:
        greeting_for_now = "Good evening"
    print(f'{greeting_for_now}! Let\'s explore some US bikeshare data!')
    return None

def get_city() -> str:
    """
    Takes input from the user to choose a city to analyse
    :return city: the city chosen for analysis
    """
    # get user input for city, allowing for future expansion of data to further cities
    while True:
        available_cities = [city for city in CITY_DATA.keys()]
        try:
            city = str(input(f'\nWhich city would you like to analyse? '
                             # f'Data currently available for {str(available_cities)}\n'
                             # f'Data currently available for {str(available_cities)[1:-2]}\n'
                             # f'Data currently available for {str(available_cities),}\n' 
                             # f'Data currently available for {*available_cities,}\n'
                             f'Data currently available for {", ".join(str(city) for city in available_cities)}\n'
                             ))
            city = city.lower()
            # TODO: implement some regex to make handling typos more elegant & robust, must be able to find some existing examples?
            # TODO: same for months and days, so maybe create a separate reusable typos function?
            typos = {
                "chicgo": "chicago",
                "chiago": "chicago",
                "chicargo": "chicago",
                "new york": "new york city",
                "nyc": "new york city",
            }
            if city in typos.keys():
                print(f"Correcting typo: {city} >>> {typos[city]}")
                city = typos[city]
            if city not in available_cities:
                print(f"Apologies, data currently available for {available_cities,}")
                continue
        except ValueError:
            print(f"Apologies, I didn't understand that. Data currently available for {available_cities,}")
            continue
        else:
            # TODO: obtain min and max month & day from data to populate month and day filter prompts
            break
    return city

def get_month() -> (int, str):
    """
    Takes input from the user to choose a month to analyse
    :return month_number: an integer to represent the calendar month
    """
    # get user input for month (all, january, february, ... , june)
    # TODO: message to only handle jan-jun!
    while True:
        try:
            chosen_month = input('\nWhich month would you like to analyse?\n').lower()
            if type(chosen_month) != str:
                print(
                    'TypeError: Apologies, only strings handled, please enter a calendar month in English, e.g. January, '
                    'February, March, April, May, June, July, September, October, November or December')
                continue
            full_monthnames = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
                ]
            abb_monthnames = [name.lower()[:3] for name in full_monthnames]
            lowercase_monthnames = [name.lower() for name in full_monthnames]

            if chosen_month in lowercase_monthnames:
                chosen_month = datetime.datetime.strptime(chosen_month, "%B")
                chosen_month = chosen_month.strftime("%b").lower()
            if chosen_month in abb_monthnames:
                chosen_month = datetime.datetime.strptime(chosen_month, "%b")

                break
            elif chosen_month not in abb_monthnames:
                print(
                    "Apologies, I didn't understand that please enter a calendar month in English, e.g. January, "
                    "February, March, April, May, June, July, August, September, October, November or December")
                continue
        except TypeError:
            print('TypeError: Apologies, numbers not handled, please enter a calendar month in English, e.g. January, '
                  'February, March, April, May, June, July, August, September, October, November or December')
            continue
        except ValueError:
            print('ValueError: Please enter a calendar month in English, e.g. January, '
                  'February, March, April, May, June, July, August, September, October, November or December')
            continue
        except KeyboardInterrupt:
            print("Keyboard Interrupt - no input taken")
            break
        #finally:
            #print("Attempted input")

    month_number = chosen_month.month
    month_name = full_monthnames[month_number-1]

    return month_number, month_name

def get_day() -> (int, str):
    """
    Takes input from the user to choose a day to analyse
    :return day_number: an integer to represent the day of the week
    """
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            chosen_day = str(input('\nWhich day would you like to analyse?\n')).lower()
        except:
            print('Apologies, not understood, please enter a day of the week in English, \n '
                  'e.g. Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday')
            continue
        else:
            break

    display_daynames = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday', ]
    abb_daynames = [name.lower()[:3] for name in display_daynames]
    lowercase_daynames = [name.lower() for name in display_daynames]

    if chosen_day in display_daynames:
        day_index = display_daynames.index(chosen_day)
    if chosen_day in abb_daynames:
        day_index = abb_daynames.index(chosen_day)
    elif chosen_day in lowercase_daynames:
        day_index =lowercase_daynames.index(chosen_day)

    day_number = day_index + 1
    day_name = display_daynames[day_index]
    print(f"Day selected: {day_name}, (weekday: {day_number})")
    return day_number, day_name

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    city = get_city()
    month_number, month_name = get_month()
    day_number, day_name = get_day()

    print('-'*40)
    user_filters = {
        "city": city,
        "month_number":month_number,
        "month_name":month_name,
        "day_number":day_number,
        "day_name":day_name,
    }
    return user_filters


def load_data(user_filters):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args: (dict) user_filters, contains:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[user_filters['city']])
    #print(type(df['Start Time'][0]))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #print(type(df['Start Time'][0]))

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    print(f"{df['month'][0]}, {type(df['month'][0])}")
    print(f"{user_filters['month_number']}, {type(user_filters['month_number'])}")

    #df = df[df["month"] == user_filters['month_number']]
    #df = df[df["day_of_week"] == user_filters['day_number']-1]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel for your chosen filters...\n'
          'Chosen Filters: ')
    start_time = time.time()
    stats = df.describe()

    # TODO:intelligently show/don't show when filtered (but check rubric for requirements)
    # display the most common month
    #modes = df.mode()
    monthnames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    common_month = df.mode()['month'][0]
    print(f"The most common month in the filtered data is {monthnames[common_month-1]}")

    # display the most common day of week
    common_day = df.mode()['day_of_week'][0]
    print(f"The most popular day of the week in the filtered data is {monthnames[common_month - 1]}")

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
    greeting()
    while True:
        user_filters = get_filters()
        # city = 'chicago'
        # month_number = int(1)
        # month_name = 'january'
        # day = 'monday'
        df = load_data(user_filters)

        time_stats(df, user_filters)
        station_stats(df, user_filters)
        trip_duration_stats(df, user_filters)
        user_stats(df, user_filters)


        restart = input('\nWould you like to restart to choose different filter options?\n'
                        'Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
