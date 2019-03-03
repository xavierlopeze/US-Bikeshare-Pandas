import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

#it has been chosen to asgin monday as 0 and not in one for convinence of the datetime package function .week()
WEEKDAY = {'monday': 0,
           'tuesday':1,
           'wednesday':2,
           'thursday':3,
           'friday':4,
           'satuday':5,
           'sunday':6
          }

NUM_TO_WEEKDAY = {
            0:'Monday',
            1:'Tuesday',
            2:'Wednesday',
            3:'Thursday',
            4:'Friday',
            5:'Satuday',
            6:'Sunday'
          }

MONTH = {'january': 1,
         'february':2,
         'march':3,
         'april':4,
         'may':5,
         'june':6}

NUM_TO_MONTH = {
         1:'January',
         2:'February',
         3:'March',
         4:'April',
         5:'May',
         6:'June'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #initialize month and day (if time_filter = 'none' month and day are kept equal to zero)
    month = 0
    day = 0

    print('Hello! Let\'s explore some US bikeshare data!')

    #GET CITY
    city = input("\n Would you like to see data from Chicago, New York or Washington? \n").lower()
    while city not in CITY_DATA:
        city = input('Wrong input! \nWrite a city from the following list: Chicago, New York, Washington. \n').lower()

    #GET TYPE OF TIME FILTER
    time_filter = input('\n Would you like to filter data by day, month, or none at all?\n').lower()
    viable_input_time = ['day','month','none']

    while time_filter not in viable_input_time:
        time_filter = input('\nWrong input! \nWrite a filter type from the following list: day, month, none. \n').lower()
    #GET DAY
    if time_filter == 'day':
        day = input('\n Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. \n').lower()
        viable_input_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        while day not in viable_input_day:
            day = input('\n Wrong input! Write a day from the following list Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n').lower()
    else:
         #GET MONTH
        if time_filter == 'month':
            month = input('\n Which month? January, February, March, April, May or June ?\n').lower()
            viable_input_month = ['january', 'february', 'march','april','may','june']
            while month not in viable_input_month:
                month = input('\n Wrong input! \nWrite a month from the following list: January, February, March, April, May, June\n').lower()

    return city, time_filter, month, day


def load_data_print(start_time):
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

def load_data(city, time_filter, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("\nLoading data and preprocessing...")
    start_time = time.time()
    df = pd.read_csv(CITY_DATA[city])

    #Create columns for the dataframe for convinience in calculations
    df['start_year']  = [int(value[0:4])   for value in df["Start Time"]]
    df['start_month'] = [int(value[5:7])   for value in df["Start Time"]]
    df['start_day']   = [int(value[8:10])  for value in df["Start Time"]]
    df['start_hour']  = [int(value[11:13]) for value in df["Start Time"]]
    df['start_min']   = [int(value[14:16]) for value in df["Start Time"]]
    df['start_sec']   = [int(value[17:20]) for value in df["Start Time"]]

    df['end_year']  = [int(value[0:4])   for value in df["End Time"]]
    df['end_month'] = [int(value[5:7])   for value in df["End Time"]]
    df['end_day']   = [int(value[8:10])  for value in df["End Time"]]
    df['end_hour']  = [int(value[11:13]) for value in df["End Time"]]
    df['end_min']   = [int(value[14:16]) for value in df["End Time"]]
    df['end_sec']   = [int(value[17:20]) for value in df["End Time"]]

    #Create a new column for the dataframe containing the day of the week
    day_of_week = []
    for index, row in df.iterrows():
        day_of_week.append( dt.date(row["start_year"], row["start_month"], row["start_day"]).weekday())
    df['day_of_week'] = day_of_week

    #Apply the required filters and return the dataframe
    if time_filter == 'none':
        load_data_print(start_time)
        return df
    elif time_filter == 'month':
        df = df[(df['start_month']==MONTH[month])]
        load_data_print(start_time)
        return df
    elif time_filter == 'day':
        df = df[(df['day_of_week']==WEEKDAY[day])]
        load_data_print(start_time)
        return df
    else:
        print("\nERROR on viable_unput_time value")
        return 1



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    month_mode = NUM_TO_MONTH[df['start_month'].mode()[0]]
    print("The most common month has been " + month_mode + ".")

    # Display the most common day of week
    weekday_mode = NUM_TO_WEEKDAY[df['day_of_week'].mode()[0]]
    print("The most common day of the week has been " + weekday_mode + ".")

    # Display the most common start hour
    start_hour_mode = [df['start_hour'].mode()[0]][0]
    print("The most common hour has been at " + str(start_hour_mode) + " hours.")

    # Display the most common day
    sd_df = df[['start_year', 'start_month','start_day']]
    sd_df = sd_df.groupby(['start_day', 'start_month', 'start_year']).size().reset_index(name='counts')
    sd_df = sd_df.sort_values(by = ['counts','start_year','start_month','start_day'], ascending = [False, False, False, False ])

    cmonth, cday, cyear, ncounts = sd_df['start_month'].values[0], sd_df['start_day'].values[0], sd_df['start_year'].values[0], sd_df['counts'].values[0]
    print("The most common day has been on " + str(cday) + " " + NUM_TO_MONTH[cmonth] + " " + str(cyear) + ", having a total of " + str(ncounts)+ " bike rents.")

    #Time controlling
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    cstart_station = df['Start Station'].mode()[0]
    print("The most common start station has been " + cstart_station + ".")

    # Display most commonly used end station
    cend_station = df['End Station'].mode()[0]
    print("The most common end station has been " + cend_station + ".")

    # Display most frequent combination of start station and end station trip
    ss_df = df[['Start Station', 'End Station']]
    ss_df = ss_df.groupby(['Start Station', 'End Station']).size().reset_index(name='counts')
    ss_df = ss_df.sort_values(by = ['counts'], ascending = [False])

    ccomb_start_station, ccbom_end_station = ss_df['Start Station'].values[0], ss_df['End Station'].values[0]
    print("The most frequent combination of start station and end station trip bas been:")
    print("     -Start Station: " + ccomb_start_station)
    print("     -End Station:   " + ccbom_end_station)
    print("     Having a total of " + str(ss_df['counts'].values[0]) + ' bike rents.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # compute a column on the data frame having the travel time of each bike rent
    df['travel_time'] = df['end_sec'] - df['start_sec'] + 60*(df['end_min']-df['start_min']) + 3600*(df['end_hour']-df['start_hour'])

    # Display total travel time
    total_time = df['travel_time'].sum()
    print("The total travel time has been " + str(dt.timedelta(seconds=int(total_time))) + ".")

    # Display mean travel time
    avg_time = df['travel_time'].mean()
    print("The average travel time has been " + str(dt.timedelta(seconds=int(avg_time))) + ".")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    ut_df = df[['User Type']]
    ut_df = ut_df.groupby(['User Type']).size().reset_index(name='counts')
    ut_df = ut_df.sort_values(by = ['counts'], ascending = [False])

    for row in range(ut_df.values.shape[0]):
        counts = ut_df.values[row][1]
        user_type = ut_df.values[row][0]
        print("There has been " + str(counts) + " bike rents done by " + user_type + " users." )

    print("")

    if city == "washington":
        return 0


    # Display counts of gender

    g_df = df[['Gender']]
    g_df = g_df.groupby(['Gender']).size().reset_index(name='counts')
    g_df = g_df.sort_values(by = ['counts'], ascending = [False])

    for row in range(g_df.values.shape[0]):
        counts = g_df.values[row][1]
        gender = g_df.values[row][0]
        print("There has been " + str(counts) + " bike rents done by " + gender + " users." )


    # Display earliest, most recent, and most common year of birth
    print("\nThe earliest year of birth as been " + str(int(df['Birth Year'].min())))
    print("The most recent year of birth as been " + str(int(df['Birth Year'].max())))
    print("The most common year of birth has been " + str(int(df['Birth Year'].mode())))


    # Print end message
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    q = input(" Would you like to display some raw data?\n").lower()
    if q != "yes":
        return 0

    #Deleting custom-created rows from the dataframe, which have been 14
    original_df = df[df.columns[:-14]]

    #initialize rowcount
    rcount = 0

    while(q == "yes"):
        print(original_df.iloc[rcount : rcount + 5])
        q = input("\n Would you like to display 5 more rows?\n").lower()
        rcount += 5


def main():
    while True:
        city,time_filter, month, day = get_filters()

#         print('\n' + ''*40 + '\n')

        df = load_data(city, time_filter, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
