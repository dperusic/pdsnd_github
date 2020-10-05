import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
weekdays = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    _city, _month, _day = False, False, False
    confirm = ""

    print('-' * 50)
    print("Please specify a city, month, and day to analyze")
    print('-' * 50)
    while confirm.lower() != "yes":
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        while _city is False:
            _city = input("Name of the city to analyze (chicago, new york city, washington): ")
            if _city.lower() not in CITY_DATA:
                print(f"Your entry '{_city}' is not valid")
                _city = False
            city = _city

    # get user input for month (all, january, february, ... , june)
        while _month is False:
            _month = input("Name of the month to filter by (January to June), or 'all' to apply no month filter): ")
            if _month.lower() not in months and _month.lower() != 'all':
                print(f"Your entry '{_month}' is not valid")
                _month = False
            # dodati neki broj pokušaja - nakon 3 kriva izlazi se iz menija
            month = _month

    # get user input for day of week (all, monday, tuesday, ... sunday)
        while _day is False:
            _day = input("Name of the day of week to filter by or 'all' to apply no day filter: ")
            if _day.lower() not in weekdays and _day != 'all':
                print(f"Your entry '{_day}' is not valid")
                _day = False
            day = _day

        print(f"""Your selection is the following:
         - Selected   City: {_city}
         - Selected  Month: {_month}
         - Selected    Day: {_day}
        """)
        confirm = input("Correct [yes/no]") or "no"
        print(confirm)

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
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        _month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == _month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe

        _day = weekdays.index(day.lower()) + 1
        df = df[df['day_of_week'] == _day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month

    # find the most popular month
    popular_month = df['month'].mode()[0]
    print('Most common month:', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    popular_dayofweek = df['day_of_week'].mode()[0]
    popular_dayofweek = weekdays[popular_dayofweek - 1]
    print('Most common day of week:', popular_dayofweek)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common hour of day:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most common end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " -> " + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('Most common trip from start to end:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum(axis=0)
    print(f"Total travel time is: {total_travel_time}")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].sum(axis=0)
    print(f"Mean travel time is: {total_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    #counts of each user type   
    user_types_count = df['User Type'].value_counts()
    print(f"Count of individual User Types:\n{user_types_count}")

    #counts of each gender (only available for NYC and Chicago)
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print(f"Count of each gender:\n{gender_count}")
    else:
        print("No data available for calculation of gender count!")

    #earliest, most recent, most common year of birth (only available for NYC and Chicago)

    if 'Birth Year' in df:

        birth_year_earliest = df['Birth Year'].min(axis=0)
        print(f"Earliest year of birth: {birth_year_earliest}")

        birth_year_recent = df['Birth Year'].max(axis=0)
        print(f"Most recent year of birth: {birth_year_recent}")

        birth_year_common = df['Birth Year'].mode()[0]
        print(f"Most common year of birth: {birth_year_common}")
    else:
        print("No data available to calculate earliest, most recent, most common year of birth!")

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    """
    Printing raw data from DataFrame with 5 record steps.
    """

    start_row, end_row = 0,5
    more = input("Print raw data? [Enter 'yes' to confirm] ").lower()
    if more == 'yes':
        while more == 'yes':
            slice = df.iloc[start_row:end_row]
            print(f"Printing raw data from file, rows {start_row} to {end_row}")
            print('-'*50)
            print(slice)
            more = input("Load more data? [Enter 'yes' to confirm or 'no' to exit] ").lower()
            if more == 'yes':
                start_row +=5
                end_row +=5
            else:
                more = 'no'


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            print_raw_data(df)
        else:
            print("No data in datafile.")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
