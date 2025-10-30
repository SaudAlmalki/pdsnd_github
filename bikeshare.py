import time
import pandas as pd

# Dictionary mapping city names to their respective CSV files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():
    """
    Ask user to specify a city, month, and day to analyze.
    Allows combined filtering by both month and day.

    Returns:
        city (str): selected city name
        month (str): selected month or 'all' for no filter
        day (str): selected day or 'all' for no filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    # Get user input for city
    while True:
        city = input("Would you like to see data for Chicago, New York, or Washington? ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please choose from Chicago, New York, or Washington.")

    # Ask user for filtering options
    while True:
        filter_type = input(
            "Would you like to filter the data by month, day, both, or not at all? Type 'none' for no filter: "
        ).strip().lower()
        if filter_type in ['month', 'day', 'both', 'none']:
            break
        else:
            print("Invalid input. Please type 'month', 'day', 'both', or 'none'.")

    # Initialize default filters
    month = 'all'
    day = 'all'

    # Get month if needed
    if filter_type in ['month', 'both']:
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        while True:
            month = input("Which month - January, February, March, April, May, or June? ").strip().lower()
            if month in months:
                break
            else:
                print("Invalid month. Please try again.")

    # Get day if needed
    if filter_type in ['day', 'both']:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while True:
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").strip().lower()
            if day in days:
                break
            else:
                print("Invalid day. Please try again.")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Load and filter bikeshare data based on city, month, and day.

    Args:
        city (str): City name ('chicago', 'new york', 'washington')
        month (str): Month name or 'all'
        day (str): Day name or 'all'

    Returns:
        df (DataFrame): Filtered pandas DataFrame
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert 'Start Time' column to datetime for time-based operations
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day, and hour from 'Start Time'
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day if applicable
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df


def time_stats(df):
    """
    Display statistics on the most frequent times of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert month numbers back to names for better readability
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    # Display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', months[common_month - 1])

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', common_day)

    # Display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def station_stats(df):
    """
    Display statistics on the most popular stations and trips efficiently.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calculate most common start and end stations and trip in one go
    df['Trip'] = df['Start Station'] + " → " + df['End Station']
    most_common = df.agg({
        'Start Station': lambda x: x.mode()[0],
        'End Station': lambda x: x.mode()[0],
        'Trip': lambda x: x.mode()[0]
    })

    print('Most Common Start Station:', most_common['Start Station'])
    print('Most Common End Station:', most_common['End Station'])
    print('Most Common Trip:', most_common['Trip'])

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def trip_duration_stats(df):
    """
    Display statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total Travel Time:', df['Trip Duration'].sum())
    print('Average Travel Time:', df['Trip Duration'].mean())

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def user_stats(df):
    """
    Display statistics on bikeshare users, including user type, gender, and birth year if available.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types:\n', df['User Type'].value_counts())

    # Display counts of gender (if available)
    if 'Gender' in df.columns:
        print('\nGender Count:\n', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth (if available)
    if 'Birth Year' in df.columns:
        print('\nEarliest Year:', int(df['Birth Year'].min()))
        print('Most Recent Year:', int(df['Birth Year'].max()))
        print('Most Common Year:', int(df['Birth Year'].mode()[0]))

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def display_raw_data(df):
    """
    Display raw data upon user request in increments of 5 rows.
    """
    i = 0
    show_data = input("Would you like to see 5 lines of raw data? (yes/no): ").lower()
    while show_data == 'yes':
        print(df.iloc[i:i + 5])
        i += 5
        show_data = input("Would you like to see 5 more rows? (yes/no): ").lower()


def main():
    """
    Main function controlling the program flow.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Call analysis functions
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
