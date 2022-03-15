import re
import time
from parse import *
import datetime
import pandas as pd
import numpy as np

from constants import DATAPATH
from constants import CITY_DATA
from constants import MONTHNAMES
from constants import WEEKDAYS

# TODO: change weekdays and months in constants to tuples

# TODO: regex useful in user inputs &/or typos?
# https://getpocket.com/read/2965365121
# regex 101?
# https://ryanstutorials.net/regular-expressions-tutorial/
# TODO: lookup Rich and Textual, re improving the terminal UI
# https://github.com/Textualize/textual
# https://rich.readthedocs.io/en/stable/introduction.html

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

def tidy_input(user_input:str) -> str:
    '''
    Tidies the user's initial input:
    :param user_input:
    :return: user_input
    '''
    # remove whitespace
    user_input = user_input.strip()
    # all lowercase
    user_input = user_input.lower()
    # remove duplicated spaces (useful for new york city)
    user_input = " ".join(user_input.split())

    return user_input

def get_city() -> str:
    """
    Takes input from the user to select a city for analysis
    :return city: The city chosen for analysis
    """
    # get user input for city, allowing for future expansion of data to further cities
    while True:
        available_cities = [city for city in CITY_DATA.keys()]
        try:
            city = str(input(f'\nWhich city would you like to analyse? '
                             f'Data currently available for {", ".join(str(city) for city in available_cities)}\n'
                             ))
            city = tidy_input(city)
            typos = {
                "chicgo": "chicago",
                "chiago": "chicago",
                "chicargo": "chicago",
                "new york": "new york city",
                "nyc": "new york city",
                "newyorkcity": "new york city",
                "newyork": "new york city",
                "ny city": "new york city",
                "nycity": "new york city",
            }
            if city in typos.keys():
                print(f"City identified: {city} >>> {typos[city].title()}")
                city = typos[city]
            if city not in available_cities:
                abb_cities = [name.lower()[:3] for name in available_cities]
                if city in abb_cities:
                    city = available_cities[abb_cities.index(city)]
                    break
                print(f"Apologies, data only currently available for {available_cities,}")
                continue
        except ValueError:
            print(f"Apologies, I didn't understand that. Data currently available for {available_cities,}")
            continue
        else:
            break
    print(f"City selected: {city.title()}")
    return city

def get_month(monthnames=MONTHNAMES) -> (int, str):
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
                    'TypeError: Apologies, only strings handled, please enter an available calendar month in English, e.g. January')
                continue

            abb_monthnames = [name.lower()[:3] for name in monthnames]
            # lowercase_monthnames = [name.lower() for name in MONTHNAMES]

            if chosen_month in [name.lower() for name in monthnames]:
                chosen_month = datetime.datetime.strptime(chosen_month, "%B")
                chosen_month = chosen_month.strftime("%b").lower()
            if chosen_month in abb_monthnames:
                chosen_month = datetime.datetime.strptime(chosen_month, "%b")
                break
            elif chosen_month not in abb_monthnames:
                print(
                    "Apologies, I didn't understand that please enter an available calendar month in English, e.g. January")
                continue
        except TypeError:
            print('TypeError: Apologies, numbers not handled, please enter an available calendar month in English, e.g. January')
            continue
        except ValueError:
            print('ValueError: Please enter an available calendar month in English, e.g. January')
            continue
        except KeyboardInterrupt:
            print("Keyboard Interrupt - no input taken")
            break
        #finally:
            #print("Attempted input")

    month_number = chosen_month.month
    month_name = MONTHNAMES[month_number-1]

    print(f"Month selected: {month_name.capitalize()}, (month number: {month_number})")

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
            if chosen_day[:3] in [day.lower()[:3] for day in WEEKDAYS]:
                break
            else:
                continue
        except:
            print('Apologies, not understood, please enter a day of the week in English, \n '
                  'e.g. Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday')
            continue
        # else:
        #     break


    # abb_daynames = [name.lower()[:3] for name in WEEKDAYS]
    # lowercase_daynames = [name.lower() for name in WEEKDAYS]

    # if "day" in chosen_day:
    #     chosen_day = search('{}day', chosen_day)[0]

    # if chosen_day in display_daynames:
    #     day_index = display_daynames.index(chosen_day)
    # if chosen_day[:3] in [day.lower()[:3] for day in WEEKDAYS]:
    #     day_index = [day.lower()[:3] for day in WEEKDAYS].index(chosen_day[:3])
    # # elif chosen_day in lowercase_daynames:
    #     day_index =lowercase_daynames.index(chosen_day)
    day_index = [day.lower()[:3] for day in WEEKDAYS].index(chosen_day[:3])
    day_number = day_index + 1
    day_name = WEEKDAYS[day_index]
    print(f"Day selected: {day_name.capitalize()}, (weekday: {day_number})")
    return day_number, day_name

def get_filters() -> dict:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    city = get_city()

    while True:
        try:
            chosen_filters = input('\nWould you like to filter by month, day or both?\n').lower()
            if 'mon' in chosen_filters:
                print("Month selected")
                month_number, month_name = get_month()
                day_number, day_name = 'None chosen', 'None chosen'
                break
            elif 'day' in chosen_filters:
                print("Day selected")
                day_number, day_name = get_day()
                month_number, month_name = 'None chosen', 'None chosen'
                break
            elif 'both' in chosen_filters:
                print("Both selected")
                month_number, month_name = get_month()
                day_number, day_name = get_day()
                break
            else:
                print("No filters recognised, options are 'month', 'day' or 'both'")
                continue

        #todo: does it need to handle no filters?
        except:
            print("No filters recognised, options are 'month', 'day' or 'both'")
            continue

    print('-'*40)
    user_filters = {
        "city": city,
        "month_number":month_number,
        "month_name":month_name,
        "day_number":day_number,
        "day_name":day_name,
    }
    return user_filters

# todo: type annotations
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
    df = pd.read_csv(DATAPATH + CITY_DATA[user_filters['city']])

    #print(type(df['Start Time'][0]))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #print(type(df['Start Time'][0]))
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] = df['Start Time'].dt.month
    # Confirm that the chosen month exists in the data:
    # todo: this doesn't work if both and a non-existent month chosen?
    if 'None chosen' not in user_filters['month_name']:
        if user_filters['month_number'] not in df['month']:
            print(f"{user_filters['city']} data contains no entries for {user_filters['month_name']}")
            df.sort_values(by='month', inplace=True)
            available_month_numbers = df['month'].unique()
            available_month_names = []
            for month in available_month_numbers:
                available_month_names.append(MONTHNAMES[month-1])
            print(f"Data contains: {available_month_names}")
            user_filters['month_number'], user_filters['month_name'] = get_month(available_month_names)

    # Create additional required dataframe columns
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['start_hour'] = df['Start Time'].dt.hour
    df['journey'] = df['Start Station']+df['End Station']
    df['Journey Time'] = df['End Time'] - df['Start Time']

    #print(f"{df['month'][0]}, {type(df['month'][0])}")
    #print(f"{user_filters['month_number']}, {type(user_filters['month_number'])}")

    # Then filter by chosen user filters if applicable:
    if 'None chosen' not in user_filters['month_name']:
        df = df[df["month"] == user_filters['month_number']]
    if 'None chosen' not in user_filters['day_name']:
        df = df[df["day_of_week"] == user_filters['day_number']-1]
    return df, user_filters

# todo: type annotations
def time_stats(df, user_filters):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel for your chosen filters...\n'
          'Chosen Filters:\n'
          f'City - {user_filters["city"].title()}\n'
          f'Month - {user_filters["month_name"].capitalize()}\n'
          f'Day of the week - {user_filters["day_name"].capitalize()}\n'
          )
    start_time = time.time()
    stats = df.describe()

    if 'None chosen' in user_filters['month_name']:
        # display the most common month
        common_month = int(df.mode()['month'][0])
        print(f"Most popular month: {MONTHNAMES[common_month-1]}")

    if 'None chosen' in user_filters['day_name']:
        # display the most common day of week
        common_day = int(df.mode()['day_of_week'][0])
        print(f"Most popular day: {WEEKDAYS[common_day - 1]}")

    # display the most common start hour
    common_hour = int(df.mode()['start_hour'][0])
    print(f"Most popular hour: {common_hour}")

    #todo: round these numbers to something sensible
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# todo: take out unused user_filters or use them
def station_stats(df, user_filters):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df.mode()['Start Station'][0]
    print(f"The most popular Start Station in the filtered data is {common_start_station}")

    # display most commonly used end station
    common_end_station = df.mode()['End Station'][0]
    print(f"The most popular End Station in the filtered data is {common_end_station}")

    # display most frequent combination of start station and end station trip
    common_journey = df.mode()['journey'][0]
    print(f"The most popular journey in the filtered data is {common_journey}")

    #todo: round these numbers to something sensible
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# todo: take out unused user_filters or use them
def trip_duration_stats(df, user_filters):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Journey Time"].sum()
    print(f"The total travel time for the filtered data is {total_travel_time}")

    # display mean travel time
    mean_travel_time = df["Journey Time"].mean()
    print(f"The mean travel time for the filtered data is {mean_travel_time}")

    #todo: round these numbers to something sensible
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# todo: take out unused user_filters or use them
# todo: type annotations
def user_stats(df, user_filters):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats for your filters...\n')
    start_time = time.time()

    # Display counts of user types
    #user_type_describe = df["User Type"].describe()
    #print(user_type_describe)
    user_type_counts = df["User Type"].value_counts()
    print(f"Subscriber: {user_type_counts['Subscriber']}")
    print(f"Customer: {user_type_counts['Customer']}")

    # Display counts of gender
    if "Gender"in df:
        gender_type_counts = df["Gender"].value_counts()
        #print(gender_type_counts)
        print(f"Male: {gender_type_counts['Male']}")
        print(f"Female: {gender_type_counts['Female']}")
    else:
        print("No gender data in the city data chosen")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        earliest_dob = df["Birth Year"].min()
        print(f"Earliest birth year: {earliest_dob}")
        latest_dob = df["Birth Year"].max()
        print(f"Latest birth year: {latest_dob}")
        common_dob = df.mode()["Birth Year"][0]
        print(f"Most common birth year: {common_dob}")
    else:
        print("No Birth Year data in the city data chosen")

    #todo: round these numbers to something sensible
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
        df, user_filters = load_data(user_filters)

        time_stats(df, user_filters)
        station_stats(df, user_filters)
        trip_duration_stats(df, user_filters)
        user_stats(df, user_filters)

        display_filtered_data = input('\nWould you like to view your filtered data 5 lines at a time?\n'
                                 "(Sounds like a tedious way to view it, but I won't stop you!\n"
                        'Enter yes or no.\n')
        if display_filtered_data.lower() == 'yes':
            # TODO: make this 5 lines at a time, rather than just head
            # remember to loop
            # needs to handle typos
            print(df.head())

        display_raw_data = input('\nWould you like to view the whole dataset for your chosen city 5 lines at a time?\n'
                                 "(Sounds like a really tedious way to view it, but I won't stop you! ;-)  )\n"
                        'Enter yes or no.\n')
        if display_raw_data.lower() == 'yes':
            # TODO: make this 5 lines at a time, rather than just head
            # remember to loop
            # needs to handle typos
            raw_df = pd.read_csv(CITY_DATA[user_filters['city']])
            print(raw_df.head())

        restart = input('\nWould you like to restart to choose different filter options?\n'
                        'Enter yes or no.\n')
        if 'y' not in restart.lower():
            break
        continue



if __name__ == "__main__":
	main()
