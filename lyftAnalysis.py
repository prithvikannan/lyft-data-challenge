import pandas as pd

from datetime import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

driver_ids = pd.read_csv('driver_ids.csv')
ride_ids = pd.read_csv('ride_ids.csv')
ride_timestamps = pd.read_csv('ride_timestamps.csv')

def get_all_rides(driver_id):
    driver_rides = ride_ids[ride_ids['driver_id'] == driver_id]
    return (driver_rides)

week_start_dates = ['2016-03-28',
'2016-04-04',
'2016-04-11',
'2016-04-18',
'2016-04-25',
'2016-05-02',
'2016-05-09',
'2016-05-16',
'2016-05-23',
'2016-05-30',
'2016-06-06',
'2016-06-13',
'2016-06-20',
'2016-06-27']

def categorize_ride_by_week(date_of_ride):
    for i, date in enumerate(week_start_dates):
        if date_of_ride < date:
            return i
    if date == '2016-06-27':
        return 13


def revenue_from_ride(ride_id):
    ride = ride_ids[ride_ids['ride_id'] == ride_id]
    if len(ride) == 0:
        print('ERROR RIDE NOT FOUND')
    ride = ride.reset_index(drop=True)
    miles_traveled = ride.loc[0, 'ride_distance'] / 1609.34  # meters to miles conversion
    minutes_elapsed = ride.loc[0, 'ride_duration'] / 60.0
    revenue = miles_traveled * 1.15 + minutes_elapsed * 0.22 + 2.00 + 1.75
    prime_time = ride.loc[0, 'ride_prime_time']

    revenue = revenue + revenue * (prime_time / 100)

    if revenue < 5:
        revenue = 5
    if revenue > 400:
        revenue = 400

    return revenue


# returns ride length in seconds
# nvm they already give us this lol
def get_ride_length(id):
    oneride = ride_timestamps[ride_timestamps['ride_id'] == id]
    oneride = oneride.set_index(oneride['event'])
    start_time = oneride.loc['picked_up_at', 'timestamp'][11:]
    end_time = oneride.loc['dropped_off_at', 'timestamp'][11:]
    format = '%H:%M:%S'
    tdelta = datetime.strptime(end_time, format) - datetime.strptime(start_time, format)
    return (tdelta.total_seconds())


def create_driver_profile(driver_id):
    all_rides = get_all_rides(driver_id)
    onboard_event = driver_ids[driver_ids['driver_id'] == driver_id]
    onboard_date = str(onboard_event.iloc[0,1])
    length = len(onboard_date)
    onboard_date = (onboard_date[length - 19: length - 9])
    number_of_rides = len(all_rides)
    average_ride_duration = all_rides['ride_duration'].mean()
    average_ride_distance = all_rides['ride_distance'].mean()

    if (number_of_rides != 0):
        percentage_of_prime_rides = 100 * len(all_rides[all_rides['ride_prime_time'] != 0]) / number_of_rides
    else:
        percentage_of_prime_rides = 0

    total_revenue = 0
    for id in all_rides['ride_id']:
        total_revenue += revenue_from_ride(str(id))

    if (number_of_rides != 0):
        average_ride_revenue = total_revenue / number_of_rides
    else:
        average_ride_revenue = 0

    rides_per_week = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for id in all_rides['ride_id']:
        specific_ride = ride_timestamps[ride_timestamps['ride_id'] == id]
        if specific_ride.empty:
            print('Could not find ride ' + str(id) + ' for driver ' + str(driver_id) + ' in ride_timestamps')
            continue
        date = specific_ride.iloc[3, 2][:11]
        week_number = categorize_ride_by_week(date)
        rides_per_week[week_number - 1] += 1



    values = [driver_id, onboard_date, number_of_rides, average_ride_distance / 1609.34, average_ride_duration / 60.0,
              percentage_of_prime_rides, total_revenue, average_ride_revenue]

    for num in rides_per_week:
        values.append(num)
    return (values)


def create_all_driver_profiles():
    profiles = []
    for i, id in enumerate(driver_ids['driver_id']):
        print(i)
        profiles.append(create_driver_profile(id))


    c = ['Driver ID', 'Driver Onboard Date', 'Number of Rides', 'Average Ride Distance in Miles',
         'Average Ride Duration in Minutes', 'Percentage of Prime Rides: ', 'Total Revenue: ', 'Average Ride Revenue',
         'Week 1 Rides', 'Week 2 Rides', 'Week 3 Rides','Week 4 Rides','Week 5 Rides','Week 6 Rides','Week 7 Rides',
         'Week 8 Rides','Week 9 Rides', 'Week 10 Rides','Week 11 Rides','Week 12 Rides', 'Week 13 Rides']
    x = ['Driver ID', 'Driver Onboard Date', 'Number of Rides', 'Average Ride Distance in Miles',
         'Average Ride Duration in Minutes', 'Percentage of Prime Rides: ', 'Total Revenue: ', 'Average Ride Revenue']
    final = pd.DataFrame(profiles, columns=c)
    final = final.fillna(0)
    print(final)

    final.to_csv('allCalculatedDataWithWeeklyRidesDistributions.csv')

#print(create_driver_profile('002be0ffdc997bd5c50703158b7c2491'))
#show_all_driver_profiles()


#list of drivers that do not have all of their rides listed in ride_timestamps
'136b51093f684e15e2798e4dc1e23d0c'
'1696be121baad60c7ca8a1c8164b24ad'
'1cf6fa07dcec364af2acf257b2d3731e'
'23d3a2d0f6732d106fbc3d6079ac018d'
'2c00d6d77281fb9f97c1eb711f39b08d'
'4bbf15c7280e29c1df6edd7bf6dfa56a'
'4fc9091d4e900a41a207ee32a639d658'
'53b03eb76e7c0e268c027a6868b9394c'
'794a74f41f18a115252fd26bbd16882b'
'818ce9e1cee09531cb20bdffe3f41256'
'93be171268b14a0586c48cb488bbd5cb'
'aee6c0de9d4b4e14d92bce9e4a352748'
'b794fc307d1309b3405361f9ea4e8b1b'
'cada138c65391fd98c1835e5c518397d'
'da984ad859c4b4349544b580d532ec5a'
'e127911975277f6b07fb2521647e1031'
'e45936982498bfe7a8fcfef62bf1edc8'


#returns -1 for first and last ride weeks if no rides found
def first_last_ride_weeks(driver_id):
    all_rides = get_all_rides(driver_id)
    ride_weeks = []
    for id in all_rides['ride_id']:
        specific_ride = ride_timestamps[ride_timestamps['ride_id'] == id]
        if specific_ride.empty:
            print('Could not find ride ' + str(id) + ' for driver ' + str(driver_id) + ' in ride_timestamps')
            continue
        date = specific_ride.iloc[3, 2][:11]
        week_number = categorize_ride_by_week(date)
        ride_weeks.append(week_number)

    if ride_weeks.__len__() == 0:
        return (-1,-1)
    first_ride_week = min(ride_weeks)
    last_ride_week = max(ride_weeks)
    return (first_ride_week, last_ride_week)

def first_last_all_drivers():
    rides_list = []
    for i, id in enumerate(driver_ids['driver_id']):
        first, last = first_last_ride_weeks(id)
        rides_list.append((first, last, id))
        print(i)


    rides_df = pd.DataFrame(data=rides_list, columns = ['First Ride Week', 'Last Ride Week', 'Driver ID'])
    rides_df.to_csv('FirstAndLastRideWeekData.csv')

def load_dataset():
    data = pd.read_csv('allCalculatedDataWithWeeklyRidesDistributions.csv')
    print(data)

def get_number_of_days_driven(driver_id):
    all_rides = get_all_rides(driver_id)
    all_dates = []
    for id in all_rides['ride_id']:
        specific_ride = ride_timestamps[ride_timestamps['ride_id'] == id]
        if specific_ride.empty:
            print('Could not find ride ' + str(id) + ' for driver ' + str(driver_id) + ' in ride_timestamps')
            continue
        date = specific_ride.iloc[3, 2][:11]
        if date not in all_dates:
            all_dates.append(date)

    return all_dates.__len__()

def number_of_days_driven_all_drivers():
    days_driven_list = []
    for i, id in enumerate(driver_ids['driver_id']):
        days = get_number_of_days_driven(id)
        days_driven_list.append((days, id))
        print(i)



    rides_df = pd.DataFrame(data=days_driven_list, columns = ['Number of Days Driven', 'Driver ID'])
    print(rides_df)
    rides_df.to_csv('daysDrivenData.csv')

number_of_days_driven_all_drivers()

# data = pd.read_csv('allCalculatedDataWithWeeklyRidesDistributions.csv')
# rides = pd.read_csv('FirstAndLastRideWeekData.csv')
#
# data['First Ride Week'] = rides['First Ride Week']
# data['Last Ride Week'] = rides['Last Ride Week']
#
#
# print(data)
#
# data.to_csv('CompleteFinalCalculatedData.csv')