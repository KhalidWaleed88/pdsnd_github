import time
import pandas as pd
import numpy as np


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    # Input must be valid
    print('\nData is available for:\n- Chicago\n- New York City\n- Washington')

    while True:
        city = input('What city would you like to analyse: ').lower()

        if city not in ['chicago', 'new york city', 'washington']:
            print('Please choose a valid city.')
            continue
        break

    # Get the filter
    print('\nData can be filtered by:\n- Month\n- Day\n- None')

    while True:
        time = input('What criterion would you like to filter the data with: ')
        time = time.lower()

        if time not in ['month', 'day', 'none']:
            print('Please choose a valid filter.')
            continue
        break

    # TO DO: get user input for month (all, january, february, ... , june)
    if time == 'month':
        day = 'all'
        print('\nAvailable months are January to June (included).')

        while True:
            month = input('Which month would you like to filter with: ').lower()

            if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                print('Please choose a valid month.')
                continue
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if time == 'day':
        month = 'all'
        print()

        while True:
            day = input('Which day would you like to filter with: ').lower()

            if day not in ['saturday', 'sunday', 'monday', 'tuesday',
                           'wednesday', 'thursday', 'friday']:
                print('Please choose a valid day.')
                continue
            break

    if time == 'none':
        month, day = 'all', 'all'

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

    # convert some columns to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'],
                                      format='%Y-%m-%d %H:%M:%S')

    df['End Time'] = pd.to_datetime(df['End Time'],
                                    format='%Y-%m-%d %H:%M:%S')
    # filter by month
    if month != 'all':
        mth = {'january': 1, 'february': 2, 'march': 3, 'april': 4,
               'may': 5, 'june': 6}
        df = df[df['Start Time'].dt.month == mth[month]]

    # filter by day
    if day != 'all':
        df = df[df['Start Time'].dt.weekday_name == day.capitalize()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    by_month = df['Start Time'].dt.month
    most_month = by_month.value_counts().idxmax()

    mth = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    print(f'The Most Frequent Month: {mth[most_month]}')

    # TO DO: display the most common day of week
    by_day = df['Start Time'].dt.weekday_name
    most_day = by_day.value_counts().idxmax()
    print(f'The Most Frequent Day: {most_day}')

    # TO DO: display the most common start hour
    by_hour = df['Start Time'].dt.hour
    most_hour = by_hour.value_counts().idxmax()
    print(f'The Most Frequent Hour: {most_hour}h')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_start_station = df['Start Station'].value_counts().idxmax()
    print(f'The Most Popular Start Station: {most_start_station}')

    # TO DO: display most commonly used end station
    most_end_station = df['End Station'].value_counts().idxmax()
    print(f'The Most Popular End Station: {most_end_station}')

    # TO DO: display most frequent combination of start station
    # and end station trip
    df['trips'] = df['Start Station'] + " to " + df['End Station']
    most_trip = df['trips'].value_counts().idxmax()
    print(f'The Most Popular Trip: {most_trip}')

    df.drop(columns=['trips'], inplace=True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_traval_time = df['Trip Duration'].sum()
    print(f'The Total Travel Time is {total_traval_time:.2f} seconds')

    # TO DO: display mean travel time
    average_traval_time = df['Trip Duration'].mean()
    print(f'The Average Travel Time is {average_traval_time:.2f} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type']).count()
    num_customers = user_types.loc['Customer'].to_list()[0]
    num_subscribers = user_types.loc['Subscriber'].to_list()[0]

    print('Counts by types of users:')
    print(f'The Count of Customers: {num_customers}')
    print(f'The Count of Subscribers: {num_subscribers}')

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:

        gender = df.groupby(['Gender']).count()

        num_male = gender.loc['Male'].to_list()[0]
        num_female = gender.loc['Female'].to_list()[0]

        print('\nCount by genders of users:')
        print(f'The Count of Male users: {num_male}')
        print(f'The Count of Female Users: {num_female}')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:

        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].value_counts().idxmax()

        print('\nBirth Year Stats:')
        print(f'The Earliest Birth Year is {earliest_year}')
        print(f'The Most Recent Birth Year is {most_recent_year}')
        print(f'The Most Common Birth Year is {most_common_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw(df):
    """Displays raw data 5 lines at a time"""

    # set the index to 0
    index = 0

    # print the 1st 5 lines of data
    print(df.iloc[index: index+5])

    while True:

        answer = input('Would you like to see 5 more lines of data [yes/no] ? ')
        answer = answer.lower().strip()

        if answer not in ['yes', 'no']:
            print('Please enter a valid answer.')
            continue

        if answer == 'no':
            break

        # increment the index by 5, check its not bigger than the size of df
        index += 5
        upper_bound = min(len(df), index+5)

        # display the next 5 lines
        print(df.iloc[index: upper_bound])

        # break if we reached the end of the data frame
        if upper_bound == len(df):
            print('\nNo more raw data to display.')
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # descriptive stats
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # raw data visualization
        while True:

            answer = input('Would you like to see the 1st 5 lines of raw data [yes/no] ? ')
            answer = answer.strip().lower()

            if answer == 'yes':
                display_raw(df)
                break

            elif answer == 'no':
                break

            else:
                print('Please enter a valid answer.')
                continue

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
