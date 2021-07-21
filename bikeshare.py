import time
import pandas as pd  # my version 1.2.4
import numpy as np  # my version 1.20.2


CITY_DATA = {'chicago': 'data/chicago.csv',
             'new york city': 'data/new_york_city.csv',
             'washington': 'data/washington.csv'}

ERROR_MESSAGES = np.array([' Ha! Ha! You are funny !', 'Well that didn\'t work',
                          'Let\'s try that again.. Properly this time. Look at the options again please.',
                           'Hmm... Nope!',
                           'I wasn\'t paying attention, could you repeat that please!\nUsing only the available options ... ?!',
                           'Oh ! I didn\'t find that in my option list. Try again Please !'])

MONTH_INPUT_OPTIONS = ['All', 'January', 'February', 'March', 'April', 'May', 'June']

DAY_INPUT_OPTIONS = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                     'Friday', 'Saturday', 'Sunday']


def input_(message, lst):
    """
    Args:
        (str) message   - message to be displayed when asking for input
        (list) list     - a list used to check that the input is a value in it

    Returns :
        (str) user_input - as a option/string selected from the list
        (boolean) exact_match - returns True or False whether the user inputted
                                correctly typed option

    Input function that will print the *message and will check the user input against
        the given list.
    To minimise possible typo errors, it only checks against the first three characters
        of each option, regardless of their case.
    A 20 tries limit has been implemented just in case the user does 19 typos of the
        first three characters of the options in a row  :D
    """
    # we'll put everything in a try-except to catch user KeyboardInterrupt
    # otherwise there should be no problems (besides EOF)
    # as we are dealing only with strings

    # creating a list with the short versions of the options
    short_list = list([x[:3].lower() for x in lst])
    tries = 20
    while tries != 0:
        try:
            # ask for user input printing the *message
            inpt = str(input(message + '\n'))
            # check if the first three characters match any of the option's first three characters
            if inpt[:3].lower() in short_list:
                # return the option, plus, if the user correctly typed the whole option name
                return (lst[short_list.index(inpt[:3].lower())], inpt in lst)
            # if it doesn't match, subtract 1 from tries
            tries -= 1
            if tries > 0:
                # print random error message if no match has been found and there are tries left
                print(np.random.choice(ERROR_MESSAGES, 1))
                # the 's' accounts for the plural of time
                print('You may try {} more time{}'.format(tries, 's' * (tries > 1)))
        except KeyboardInterrupt:
            print('Alright then, see you later !!!\n:)')
            exit()
        except:
            tries -= 1
            print('No funny business !... Again !')
            print('You may try {} more time{}'.format(tries, 's' * (tries > 1)))
    print('Goodbye !!!')
    exit()


def filter(by, option):
    """
    Args:
    (str)  by   - represents the means by which the filter is applied
    (str) option- represents the actual filter

    Function takes the means by which the filter is applied (e.g. 'month' , 'day')
        and returns a string that suits each case for any particular filter or no filter.
    This should help complete a phrase with the respective text as follows

    Return examples:
    'no day filter'   or     'filter day is Monday '
    'no month filter'     or    'filter month is June'

    """
    return ((f'no {by} filter' * (option.lower() == 'all')) +
            (f'filter {by} is {option}' * (option.lower() != 'all')))


def spell_check(word):
    """
    Args:
    (tuple) - word --> (str, boolean)
        (str)       represents the correct  version of the word

        (boolean)   should be   True if the user spelled correctly or
                                False if the user made some typo

    Prints some the str from the tuple plus some text regarding the accuracy of the spelling,
        confirming the chosen option in case the input is not exactly as the option.
    """
    return '{}. Got it!'.format(word[0]) if word[1] else '{}. Close enough !'.format(word[0])


def options_str(options):
    """
    Args:
    (list) options - an list that contains the options

    Takes an iterable and returns it as a string in title case joined by commas.
    The main point of it being to get rid of the square brackets

    Returns:
    (str) A string with the options in quotes separated by commas
    """
    return ', '.join(["'" + a.title() + "'" for a in options])


def list_(tuple_list):
    """
    Args:
    (list) tuple_list - a list of tuples (trs-int pairs)

    Prints the list of tuples with two elements in a dictionary like, clean, manner,
        without parentheses, quotes or commas, skipping abnormal values.

    Returns None
    """
    for tuple in tuple_list:
        # if it's not a tuple we're not interested
        try:
            print(str(tuple[0]) + ': ' + str(tuple[1]))
        except:
            continue


def clean_column(column, min=1900, max=2020):
    """
    Args:
    (list) column   - a list with the column values
    (int)   min     - the minimum value accepted
    (int)   max     - the maximum value accepted

    This function will replace with np.nan values the values that are outside the min-max range

    Returns:
    (list) column   - the modified list
    (int)  replaced - the number of replaced values
    """
    replaced = 0
    for i, value in enumerate(column):
        if value < min or value > max:
            column[i] = np.nan
            replaced += 1
    return (column, replaced)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = [a.title() for a in CITY_DATA.keys()]

    # asks the user for input using a costum input_ function that takes a message and an option list
    city = input_('\nPlease introduce the name of the city that you would like to see information about:\n(options are: {})'.format(
        options_str(CITY_DATA.keys())),
        city_list)
    # the spell_check function only prints a custom message to doublecheck the selected option
    print(spell_check(city))

    print()
    # TO DO: get user input for month (all, january, february, ... , june)
    optionsstr = f"(options are {options_str(MONTH_INPUT_OPTIONS)}"
    month = input_('\nPlease choose the month you want to filter the dataset by, or type \'all\' for no filter\n' + optionsstr,
                   MONTH_INPUT_OPTIONS)
    print(spell_check(month))

    print()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    optionsstr = f"(options are {options_str(DAY_INPUT_OPTIONS)}"
    day = input_('\nLast filtering option, what day would you prefer filtering by, type \'All\' for all.\n' + optionsstr,
                 DAY_INPUT_OPTIONS)
    print(spell_check(day))

    print()
    print('-'*100)

    return city[0], month[0], day[0]


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # according to  user selection, read the CSV file from the CITY_DATA dictionary
    df = pd.read_csv(CITY_DATA[city.lower()])

    # transforming the date columns into pandas datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # adding month, day and hour columns to the dataframe

    df['Month'] = df['Start Time'].dt.month
    # converting month ints to names
    df['Month'] = [MONTH_INPUT_OPTIONS[i] for i in df['Month']]
    df['Day Of Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    print('\nApplying selected filters')
    if month != 'All':
        df = df[df['Month'] == month]
    if day != 'All':
        df = df[df['Day Of Week'] == day]
    print('Done')

    # verify that the user input is correct
    month_filter = filter('month', month)
    day_filter = filter('day', day)
    print()
    print(f'So, what I\'ve got from you, is:\n{city} for city, {month_filter} and {day_filter}')
    answer = input_("Is that correct? Type:\n'Yes' to continue, 'No' to change the filters, 'Look' to see the data, 'Exit' to end session.", [
        'Yes', 'No', 'Look', 'Exit'])
    print('-'*100)

    # what did he say?
    if answer[0] is 'No':
        print('\n'*5)
        main()
    if answer[0] is 'Exit':
        print('Thank You !\nCome Again!!!\nWe also serve Pizza ;)')
        exit()
    if answer[0] == 'Look':
        i = 0
        while i < len(df):
            print(df[i:i+5])
            answer = input_(
                'Want to see more?\n\'Yes\' for more, \'No\' to continue to stats', ('Yes', 'No'))
            if answer[0] == 'No':
                print('Ok then, we shall procede to the stats.')
                break
            i += 5
            print('-'*100)
    print('-'*100)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The month with the most bike rentals is unsurprisingly', df['Month'].mode()[0])
    # TO DO: display the most common day of week, sarcastically
    print('The day with the most rentals is surprisingly', df['Day Of Week'].mode()[0])
    # TO DO: display the most common start hour
    print('The hour of the day that people ride the most is', df['Hour'].mode()[0])

    # this one is a bit tricky
    # just in case   no filter has been selected for the day,
    # and the most common hour of the most common day is not the same as the most common hour overall
    # display what's the most common hour for the most common day

    # really interesting is that this condition is quite rarely true.
    # a case when all that is true for example,
    # is in Chicago in April
    # or in Washington in January

    common_day = df['Day Of Week'].mode()[0]
    common_overall_hour = df['Hour'].mode()[0]
    common_hour_of_common_day = df[df['Day Of Week'] == common_day]['Hour'].mode()[0]

    if (list(df['Day Of Week']).count(df['Day Of Week'].iloc[0]) != len(df) and
            common_hour_of_common_day != common_overall_hour):
        print("Particularly interesting, {}'s top hour is {}".format(
            common_day,
            common_hour_of_common_day))

    print("\nThis took %s seconds." % round((time.time() - start_time), 5))
    print('-'*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most popular station in town is '{}'".format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("Most often, people stop at '{}' station".format(df['End Station'].mode()[0]))
    # point out if the station is the most popular as both Start and End trip station
    if df['Start Station'].mode()[0] == df['End Station'].mode()[0]:
        print("This '{}' station seems to be very very popular here".format(
            df['Start Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    # creating a new column with trip pairs separated by  ---
    df['Trips'] = df['Start Station'] + '---' + df['End Station']
    # finding the most common trip pair and splitting into separate station names
    common_trip_stations = df['Trips'].mode()[0].split('---')
    print("People usually go from '{}' to '{}' station".format(
        common_trip_stations[0], common_trip_stations[1]))

    # analyse how many trips end and start in the starting station of
    # the most common pair of popular routes to offer a hint whether the station needs more bikes
    station_trip_from = df['Start Station'].value_counts()[common_trip_stations[0]]
    station_trip_to = df['End Station'].value_counts()[common_trip_stations[0]]

    # if more than 10% of the total trips of this station are starting from here
    # as compared to the number of trips that end here,
    # print that the station is in need of bikes,
    # or the opposite if there is more than 10% difference the other way around
    if station_trip_from >= (station_trip_to * 1.1):
        print("\n...pssst, if you are the boos of the company,'{}' station might need more bikes..".format(
            common_trip_stations[0]))
        print('{} trips start from here and {} trips ends here.'.format(
            station_trip_from, station_trip_to))
        print("{:.2f}% more rides starts here than ends here".format(
            -((1 - station_trip_from / station_trip_to) * 100)))

    if station_trip_to > (station_trip_from * 1.1):
        print("\n...psst, if you are the boss of the company,'{}' station might have an excess of bikes..".format(
            common_trip_stations[0]))
        print('{} trips start from here and {} trips ends here.'.format(
            station_trip_from, station_trip_to))
        print("{:.2f}% more trips ends here than starts from here...".format(
            -((1 - station_trip_to / station_trip_from) * 100)))

    # the information about the trips are already in the DataFrame so we are going to
    # delete the 'Trips' column as it's no longer necessary, and it saves a bit of space
    df.pop('Trips')

    print("\nThis took %s seconds." % round((time.time() - start_time), 5))
    print('-'*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # creating a new column with the difference between start and stop times as timedeltas
    df['Trip Duration'] = df['End Time'] - df['Start Time']
    print('Total duration of all trips : {}'.format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print('The average duration per trip : {} minutes'.format(
        round(df['Trip Duration'].mean().total_seconds()/60, 2)))

    print("\nThis took %s seconds." % round((time.time() - start_time), 5))
    print('-'*100)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('There are {} types of users, here\'s their type and how many of each:'.format(
        len(df['User Type'].value_counts())))
    # we are going to help ourselves with this function that prints a list more clean
    list_(df['User Type'].value_counts().items())
    print()

    # TO DO: Display counts of gender
    # test to see if the column 'Gender' exists , if so, print stats
    if df.get(['Gender'], 0) is not 0:
        print('Of the people that rented the bikes, there were:')
        list_(df['Gender'].value_counts().items())
        nan_counts = df['Gender'].isnull().sum().sum()
        # if any NaN values are present, inform the user
        if nan_counts:
            print('(You should know that in this column, there are {} missing values)'.format(nan_counts))
    else:
        print('No gender information found in this dataset')
    print()

    # TO DO: Display earliest, most recent, and most common year of birth
    # test for 'Birth Year' column to print info
    if df.get(['Birth Year'], 0) is not 0:
        # vaguely test for outliers and clean the data a bit
        print("Let's look at the 'Birth Year' column...")
        if df['Birth Year'].min() < 1907 or df['Birth Year'].max() > 2015:
            # bc stands for  before cleaning :D
            earliest_year_bc = df['Birth Year'].min()
            average_year_bc = df['Birth Year'].mean()
            latest_year_bc = df['Birth Year'].max()
            abnormal_values = (df[df['Birth Year'] < 1907]['Birth Year'].count() +
                               df[df['Birth Year'] > 2015]['Birth Year'].count())
            # the next line will show the 's' and the alternate ending only if abnormal_values > 1
            print('--Hmm.. found {} abnormal value{}, smaller than 1917... like {}{}.'.format(
                abnormal_values,
                ('s' if (abnormal_values > 1) else ''),
                earliest_year_bc,
                (', that\'s the smallest.' if (abnormal_values > 1) else '')))

            print('--Probably from typos or somebody lied in their profile or something...')
            print("--Supposing you'd agree, I will delete them so the stats are more realistic")
            cleaned_column = clean_column(list(df['Birth Year']), min=1907, max=2015)
            df['Birth Year'] = cleaned_column[0]
            print('--I have replaced with NaN values {} entries'.format(cleaned_column[1]))
            print('--We\'re good to go!\n')
            print('Back to the business')
            print('Here are the earliest, average and latest year of birth before cleaning the data:')
            print('Earliest year of birth:', earliest_year_bc)
            print('The average value of birth years:', round(average_year_bc, 2))
            print('The latest year of birth:', latest_year_bc)
            print('\nAnd now let\'s see how the data looks after cleaning (hopefully more realistic):')

        # ac stands for after cleaning, however, the actual cleaning is conditional
        earliest_year_ac = df['Birth Year'].min()
        average_year_ac = df['Birth Year'].mean()
        latest_year_ac = df['Birth Year'].max()
        print('The oldest person was born in', earliest_year_ac)
        print('The average year of birth', round(average_year_ac, 2))
        print('The youngest of them all was born in', latest_year_ac)
    else:
        print('Couldn\'t find anything on the birth year of the bike riders')
    print("\nThis took %s seconds." % round((time.time() - start_time), 5))
    print('-'*100)


def main():
    while True:
        # since the point of displaying blocks of DataFrame is to see the columns and rows
        # we set the max_columns pandas option to show all the columns
        pd.set_option('max_columns', None)
        print('\n' * 30)
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        try:
            restart = input('\nWould you like to restart? Enter \'yes\' or \'no\'.\n')
            if restart.lower() != 'yes':
                print('See you around !!!')
                break
        except:
            print('Have a nice day !')
            break


if __name__ == "__main__":
    main()
