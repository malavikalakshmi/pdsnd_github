import time
import pandas as pd
import numpy as np
from scipy import stats
"""
Help reference links - Pandas official website - https://pandas.pydata.org/pandas-docs/stable/reference/io.html
"""
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("enter the city you want to explore:list:chicago, new york city, washington").lower()
    cities = ['chicago','new york city','washington']
    while city not in cities or city is int:
        print("please check your city you have entered: Either it is numeric or not in the cities list -\nplease enter cities mentioned here in this list:chicago, new york city, washington")
        city = input("please enter city again").lower()
    print("You have entered the city {}".format(city))
    print('-'*40)
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("enter the month you want to explore :  Month or all months  - please enter 01 for January, 02 for February, 03 for March, 04 for April, 05 for May, 06 for June and 0 for all months")
    months = ['01','02','03','04','05','06','0']
    while month not in months:
        print("please check the month you have entered. Valid values - 01 for January, 02 for February, 03 for March, 04 for April, 05 for May, 06 for June and 0 for all months")
        month = input("please enter month again")
    print("You have entered the month identifier{}".format(month))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("enter the day of the week you want to explore: 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','all'")
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','all']
    while day not in days:
        print("please check the day of week you have entered. Valid values - 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','all'")
        day = input("please enter day again")
    print("You have entered the day {}".format(day))


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
    res = CITY_DATA[city]
    df_import = pd.read_csv(str(res))
    df_import['Start Time'] = pd.to_datetime(df_import['Start Time'])
    #strftime- to get in our own format
    df_import['mnth'] = df_import['Start Time'].apply(lambda x: x.strftime('%m'))
    df_import['Start Time'] = pd.to_datetime(df_import['Start Time'])
    df_import['day_of_week'] = df_import['Start Time'].dt.day_name()
    if month == '0' and day == 'all':
        return df_import
    else:
        df_modified = getFilteredData(df_import,month,day)
        return df_modified

def getFilteredData(df_import,month,day):
    """
    The fucntion filters the data frame based on the input filters selected by user.
    Args:
        (str) df_import - data frame after added 2 new columns to the original data frame -mnth & day_of_week
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing filtered by month and day
    """
    if month != '0' and day == 'all':
        new_df_modified = df_import[df_import.mnth == month]
        return new_df_modified
    elif month == '0' and day != 'all':
        print(df_import['day_of_week'].value_counts())
        new_df_modified = df_import[df_import.day_of_week == day]
        print(new_df_modified.head())
        return new_df_modified
    elif month != '0' and day != 'all':
        new_df_modified = df_import[df_import.mnth == month]
        new_df_modified = new_df_modified[new_df_modified.day_of_week == day]
        return new_df_modified


def time_stats(df,city,month,day):

    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months_dict ={"01":"January","02":"February","03":"March","04":"April","05":"May","06":"june"}
    if month == '0':
        mode_calculated_df = df.mnth.mode()
        mode_calculated = mode_calculated_df.iloc[0]
        print("Most common month for the city {} is {}".format(city,months_dict[mode_calculated]))
    else:
        print("You have already filtered the data based on the month {}.Hence, the most common month in this case is {}".format(months_dict[month],months_dict[month]))

    # TO DO: display the most common day of week
    if day == 'all':
        mode_calculated_df_day = df.day_of_week.mode()
        mode_calculated_day = mode_calculated_df_day.iloc[0]
        print("Most common day of the week {} is {}".format(city,mode_calculated_day))
    else:
        print("You have already filtered the data based on the day {}.Hence, the most common day in this case is{}".format(day,day))

    # TO DO: display the most common start hour
    def get_hours_from_start_date(ts):
        """
        This function fetches hour part of the date timestamp of Start Date column in the data frame
        Args:
        (timestamp) ts - timestamp- start date of each row of the data frame
        Returns:
        Hour part of the date timestamp
        """
        return ts.hour
    df['Start_Hours'] = df['Start Time'].apply(get_hours_from_start_date)
    mode_calculated_df_hour = df.mode()
    mode_calculated_hour = mode_calculated_df_hour.iloc[0]
    print("The most common start hour (24 hour clock standard) of the selection made by you - {},{},{} is {}.".format(city,month,day,mode_calculated_hour['Start_Hours']))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    df.columns = df.columns.str.replace(' ', '_')
    mode_calculated_df_ss = df.Start_Station.mode()
    mode_calculated_ss = mode_calculated_df_ss.iloc[0]
    print("Most most commonly used start station is {}".format(mode_calculated_ss))

    # TO DO: display most commonly used end station
    mode_calculated_df_es = df.End_Station.mode()
    mode_calculated_es = mode_calculated_df_es.iloc[0]
    print("Most most commonly used start station is {}".format(mode_calculated_es))

    # TO DO: display most frequent combination of start station and end station trip
    # first grouping by the 2 columns that we want
    #size function gives the count of each group
    #sort function arranges all the group combinations in descending order
    #first element in this will be our required combination
    new_df = df.groupby(['Start_Station','End_Station']).size().sort_values(ascending = False)
    print("The most frequent combination of start station and end station trip is {} and number of times it appears in the dataset is {}".format(new_df.index[0],new_df[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    trip_df_tot_duration = df['Trip_Duration'].sum(skipna = True)
    print("total travel time is {}".format(trip_df_tot_duration))

    # TO DO: display mean travel time
    trip_df_mean_duration = df['Trip_Duration'].mean(skipna = True)
    print("mean travel time is {}".format(trip_df_mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User_Type' in df.columns:
        count_user_types = df['User_Type'].value_counts(dropna=False)
        print("count of user types is \n{}".format(count_user_types))
    else:
          print("There is no user type data available for your selected combination of city, month and day of week")
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        count_user_gender = df['Gender'].value_counts(dropna=True)
        print("count of gender types is \n{}".format(count_user_gender))
    else:
        print("There is no gender data available for your selected combination of city, month and day of week")


    # TO DO: Display earliest, most recent, and most common year of birth
   # ifdf.isnull().sum().sort_values(ascending = False)
    if 'Birth_Year' in df.columns:
        min_dob = df['Birth_Year'].min(skipna = True)
        max_dob = df['Birth_Year'].max(skipna = True)
        mode_dob = df['Birth_Year'].mode()
        print(" Earliest, most recent year of birth are {},{}".format(min_dob,max_dob))
        print(" Most common year of birth is {}".format(mode_dob))
    else:
         print("There is no birth year data available for your selected combination of city, month and day of week")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
         #original_dataframe_after_initial_modification
        filteredModData = df.copy(deep = True)
        if df.empty == False:
            time_stats(df,city,month,day)
            raw_input_option = input("Do you wish to see top 5 rows of raw data with filters given by you inititally?- y or n").lower()
            if raw_input_option == 'y':
                print(filteredModData.head())
            else:
                print("you have selected no for printing raw data after applying initial filters or you have entered a wrong key as an answer.")
            station_stats(df)
            trip_duration_stats(df)
            raw_input_option_again = input("Do you wish to see top 5 rows of raw data with filters given by you inititally?- y or n").lower()
            if raw_input_option_again == 'y':
                print(filteredModData.head())
            else:
                print("you have again selected no for printing raw data after applying initial filters or you have entered a wrong key as an answer.")
            user_stats(df)
        else:
            print("Your current combination of selections have returned an empty dataset")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
