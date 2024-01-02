import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


def load_data():

    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see bikeshare data for Chicago, New York or Washington?').lower()
    while city !='chicago' and city !='new york' and city !='washington':
        print('That was not a valid input')
        city = input('Would you like to see bikeshare data for Chicago, New York or Washington?').lower()
    #print(city)

    data_set = CITY_DATA.get(city)
    if data_set:
        df1 = pd.read_csv(data_set)

        print('The {} data set has been loaded'.format(city))
    else:
        print('Invalid city. File not found')

    return city

def get_filters(city):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    filter_question = input('Would you like to filter the data set? Yes or No? ').lower()
    while filter_question != 'yes' and filter_question != 'no':
        print('invalid input')
        filter_question = input('Would you like to filter the data set? Yes or No? ').lower()

    if filter_question == 'yes':
        # TO DO: get user input for month (all, january, february, ... , june)
        month = input('Which month would you like to look at? All, Jan, Feb, Mar, Apr, May or Jun?').lower()
        while month !='all' and month !='jan' and month !='feb' and month !='mar' and month !='apr' and month !='may' and month !='jun':
            print('That was not a valid input')
            month = input('Which month would you like to look at? All, Jan, Feb, Mar, Apr, May or Jun?').lower()
        #print(month)

        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('For which day of the week would you like to view data? All, Mon, Tue, Wed, Thu, Fri, Sat, Sun?').lower()    
        while day !='all' and day !='mon' and day !='tue' and day !='wed' and day !='thur' and day !='fri' and day !='sat' and day !='sun': 
            print('That was not a valid input')
            day = input('For which day of the week would you like to view data? All, Mon, Tue, Wed, Thu, Fri, Sat, Sun?').lower()  
        #print(day)

    elif filter_question == 'no':
        month = 'all'
        day = 'all'
        raw_data_q = input('Would you like to see the raw data or calculate the statistics for the raw table? Answer \'raw table\' or \'stats\'').lower()

        while raw_data_q != 'raw table' and raw_data_q != 'stats':
            print('invalid input')
            raw_data_q = input('Would you like to see the raw data or calculate the statistics for the raw table? Answer \'raw table\' or \'stats\'').lower()

        if raw_data_q == 'raw table':
            # Load the entire data frame
            data_set = CITY_DATA.get(city)
            df1 = pd.read_csv(data_set)

           # Initialize starting index and batch size
            index = 0
            batch_size = 5

            # Prompt the user for input
            five_lines = input("Would you like to see 5 lines of raw data? (yes/no): ")

            while five_lines.lower() != 'yes' and five_lines.lower() != 'no':
                print('invalid input')
                five_lines = input("Would you like to see 5 lines of raw data? (yes/no): ")

            # Continue iterating until the user says 'no' or there is no more data
            while five_lines.lower() == 'yes' and index < len(df1):
                # Retrieve the next batch of rows
                batch = df1.iloc[index:index+batch_size]
                print(batch)

                # Update the index for the next batch
                index += batch_size

                # Prompt the user for input again
                five_lines = input("Would you like to see the next 5 lines of raw data? (yes/no): ")
                while five_lines.lower() != 'yes' and five_lines.lower() != 'no':
                    print('invalid input')
                    five_lines = input("Would you like to see 5 lines of raw data? (yes/no): ")

            if five_lines.lower() == 'no':
                raw_data_q = input('Would you like to calculate the statistics for the raw table? Answer \'stats\'').lower()
                while raw_data_q.lower() != 'stats':
                    print('invalid input')
                    raw_data_q = input('Would you like to calculate the statistics for the raw table? Answer \'stats\'').lower()

        elif raw_data_q == 'stats':
            print('Let\'s calculate some statistics')


    print('-'*40)
    return month, day

def load_filtered_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    data_set = CITY_DATA.get(city)
    if data_set:
        df1 = pd.read_csv(data_set)

        print('The {} data set has been loaded'.format(city))
    else:
        print('Invalid city. File not found')
    
    # Convert the 'Start Time' column to datetime format    
    df1['Start Time'] = pd.to_datetime(df1['Start Time'])

    ## extract month and day from the Start Time column to create a month and day column
    df1['Month'] = df1['Start Time'].dt.strftime('%b').str.lower()
    df1['Day'] = df1['Start Time'].dt.strftime('%a').str.lower()

    if month != 'all' and day != 'all':
        filtered_df1 = df1[(df1['Month'] == month) & (df1['Day'] == day)]
    elif month == 'all' and day != 'all':
        filtered_df1 = df1[df1['Day'] == day]
    elif month != 'all' and day == 'all':
        filtered_df1 = df1[df1['Month'] == month]
    else:
        filtered_df1 = df1
    row_count = len(filtered_df1)
    print('\n number of rows in the {} table are:'.format(city), row_count)
    print('-'*40)
    return filtered_df1
    


def time_stats(df,city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel for the entire data set...\n')
    start_time = time.time()

    data_set = CITY_DATA.get(city)
    if data_set:
        df2 = pd.read_csv(data_set)

        #print('The {} data set has been loaded'.format(city))
    else:
        print('Invalid city. File not found')

    row_count = len(df2)
    print('\n number of rows in the table are:', row_count)


    # Convert the 'Start Time' column to datetime format 
    df2['Start Time'] = pd.to_datetime(df2['Start Time'])
    
    ## extract month, day, hour from the Start Time column to create a month, day, hour column
    df2['Month'] = df2['Start Time'].dt.strftime('%b')
    df2['Day'] = df2['Start Time'].dt.strftime('%a')
    df2['Hour'] = df2['Start Time'].dt.hour

    # TO DO: display the most common month
    popular_month = df2['Month'].mode()[0]
    print('\nMost Popular Month:', popular_month)

    # TO DO: display the most common day of week
    popular_day = df2['Day'].mode()[0]
    print('\nMost Popular Day:', popular_day)

    # TO DO: display the most common start hour
    popular_hour = df2['Hour'].mode()[0]
    print('\nMost Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return df2

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    row_count = len(df)
    print('\n number of rows in the table are:', row_count)

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost Popular Start Station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost Popular End Station:', popular_start_station)

    # TO DO: display most frequent combination of start station and end station trip
    #df['Journey'] = pd.concat([df['Start Station'], df['End Station']], axis=1)
    #popular_journey = df['Journey'].mode()[0]

    df['Journey'] = df['Start Station'] +" to " + df['End Station']
    popular_journey = df['Journey'].mode()[0]
    print('\nMost Popular Journey:', popular_journey)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    row_count = len(df)
    print('\n number of rows in table are:', row_count)

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\n Total trip duration:', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\n Average trip duration:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    row_count = len(df)
    print('\n number of rows in table are:', row_count)

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\n number of user types:', user_types)

    if city != 'washington':
        # TO DO: Display counts of gender
        gender_types = df['Gender'].value_counts()
        print('\n number of gender types:', gender_types)

        # TO DO: Display earliest, most recent, and most common year of birth
        # Convert the 'Birth Year' column to datetime format 
        #df['Birth Year'] = pd.to_datetime(df['Birth Year'])

        earliest_date = df['Birth Year'].min()
        print('\n Earliest birth year of customers:', earliest_date)

        most_recent_date = df['Birth Year'].max()
        print('\n Most recent birth year of customers:', most_recent_date) 

        most_common_date = df['Birth Year'].mode()[0]
        print('\n Most common birth year of customers:', most_common_date) 

        #print("\nThis took %s seconds." % (time.time() - start_time))
        #print('-'*40)

    #else:
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    # Initialize starting index and batch size
    index = 0
    batch_size = 5

    # Prompt the user for input
    five_lines_data = input("Would you like to see 5 lines of raw data? (yes/no): ")

    while five_lines_data.lower() != 'yes' and five_lines_data.lower() != 'no':
        print('invalid input')
        five_lines_data = input("Would you like to see 5 lines of raw data? (yes/no): ")

    # Continue iterating until the user says 'no' or there is no more data
    while five_lines_data.lower() == 'yes' and index < len(df):
        # Retrieve the next batch of rows
        batch = df.iloc[index:index+batch_size]
        print(batch)

        # Update the index for the next batch
        index += batch_size

        # Prompt the user for input again
        five_lines_data = input("Would you like to see the next 5 lines of data? (yes/no): ")
        while five_lines_data.lower() != 'yes' and five_lines_data.lower() != 'no':
            print('invalid input')
            five_lines_data = input("Would you like to see 5 lines of raw data? (yes/no): ")

    '''if five_lines.lower() == 'no':
        raw_data_q = input('Would you like to calculate the statistics for the raw table? Answer \'stats\'').lower()
        while raw_data_q.lower() != 'stats':
            print('invalid input')
            raw_data_q = input('Would you like to calculate the statistics for the raw table? Answer \'stats\'').lower()

    elif raw_data_q == 'stats':
        print('Let\'s calculate some statistics')
'''

    print('-'*40)

def main():
    while True:
        city = load_data()
        month, day = get_filters(city)
        df = load_filtered_data(city, month, day)
        time_stats(df, city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

