import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITIES = ['chicago','new york city', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Would you like to see data for chicago, New York city or Washington? \n").lower()
        if city in CITIES:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Wich month? Please type (january, february,...,june or all) \n").lower()
        if month in MONTHS:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Wich day? Please type (monday, tuesday,...,sunday or all) \n").lower()
        if day in DAYS:
            break

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
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #filter data by month
    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    #filter data by day week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['month'].mode()[0]
    print('The most common month is: {}'.format(most_month))

    # display the most common day of week
    most_day = df['day_of_week'].mode()[0]
    print('The most common day of week is: {}'.format(most_day))

    # display the most common start hour
    most_hour = df['hour'].mode()[0]
    print('The most common hour is: {}'.format(most_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station is: {}'.format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('The most commonly used end station is: {}'.format(end_station))

    # display most frequent combination of start station and end station trip
    start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}".format(start_end_station[0], start_end_station[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_total = df['Trip Duration'].sum()
    print("The total travel time : {}".format(travel_total))

    # display mean travel time
    travel_moyen = df['Trip Duration'].mean()
    print("The mean travel time : {}".format(travel_moyen))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    #print the total numbers of users types one by one
    for index, user_type in enumerate(user_type_counts):
        print(" {}: {}".format(user_type_counts.index[index], user_type))


    # Display counts of gender
    if 'Gender' in df.columns:
        user_gender_counts = df['Gender'].value_counts()
    #print the total numbers of users gender one by one
        for index, user_gender in enumerate(user_gender_counts):
            print(" {}: {}".format(user_gender_counts.index[index], user_gender))
    else:
        print("There are no data for gender for this city")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        year_of_birth = df['Birth Year']

    # the most earliest year of birth
        earl_year = year_of_birth.min()
        print("The most earliest year of birth is: {}".format(earl_year))

    # the most recent year of birth
        recent_year = year_of_birth.max()
        print("The most recent year of birth is: {}".format(recent_year))

    # the most common year of birth
        common_year = year_of_birth.value_counts().idxmax()
        print("The most common year of birth is: {}".format(common_year))
    else:
        print("There are no data for birth year for this city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_data_display(df):
    longueur = df.shape[0]

    #showing 5 lines
    for i in range(0, longueur, 5):
        yes = input("Would you like to display the raw data for a particular trip? (Type 'yes' or 'no')\n").lower()
        if yes != 'yes':
            break
    #here I use json to collect data, convert them and split them
        raw_data = df.iloc[i: i+5].to_json(orient='records', lines=True).split('\n')
        for i in raw_data:
            ligne = json.loads(i)
            json_ligne = json.dumps(ligne, indent=3)
            print(json_ligne)

#Let's explore some useful informations about data

def stats_infos (df):
    print("\n")
    print("Now see two important informations about missing values:\n")
    # counts the number of missing values
    miss_values_nbr = np.count_nonzero(df.isnull())
    print("The number of missing values is: {}".format(miss_values_nbr))

    # counts the number of missing values of user type variable
    miss_values_nbr_type = np.count_nonzero(df['User Type'].isnull())
    print("The number of missing values for user type : {}".format(miss_values_nbr_type))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        user_data_display(df)
        stats_infos (df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
