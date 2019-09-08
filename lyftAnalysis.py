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

def revenue_from_ride(ride_id):
    ride = ride_ids[ride_ids['ride_id'] == ride_id]
    if len(ride) == 0:
        print('ERROR RIDE NOT FOUND')
    ride = ride.reset_index(drop=True)
    miles_traveled = ride.loc[0, 'ride_distance'] / 1609.34 #meters to miles conversion
    minutes_elapsed = ride.loc[0, 'ride_duration'] / 60.0
    revenue = miles_traveled * 1.15 + minutes_elapsed * 0.22 + 2.00 + 1.75
    prime_time = ride.loc[0, 'ride_prime_time']

    revenue = revenue + revenue * (prime_time / 100)

    if revenue < 5:
        revenue = 5
    if revenue > 400:
        revenue = 400

    return revenue

#returns ride length in seconds
#nvm im a dumbass they already give us this lol
def get_ride_length(id):
    oneride = ride_timestamps[ride_timestamps['ride_id'] == id]
    oneride = oneride.set_index(oneride['event'])
    start_time = oneride.loc['picked_up_at', 'timestamp'][11:]
    end_time = oneride.loc['dropped_off_at', 'timestamp'][11:]
    format = '%H:%M:%S'
    tdelta = datetime.strptime(end_time, format) - datetime.strptime(start_time, format)
    return(tdelta.total_seconds())


def create_driver_profile(driver_id):
    all_rides = get_all_rides(driver_id)
    # print(all_rides)
    number_of_rides = len(all_rides)
    average_ride_duration = all_rides['ride_duration'].mean()
    average_ride_distance = all_rides['ride_distance'].mean()

    if (len(all_rides) != 0):
        percentage_of_prime_rides = 100 * len(all_rides[all_rides['ride_prime_time'] != 0]) / len(all_rides)
    else:
        percentage_of_prime_rides = 0
        
    total_revenue = 0
    for id in all_rides['ride_id']:
        total_revenue += revenue_from_ride(str(id))

    if (len(all_rides) != 0):
        average_ride_revenue = total_revenue/len(all_rides)
    else:
        average_ride_revenue = 0

    values = [driver_id, number_of_rides, average_ride_distance/1609.34, average_ride_duration/60.0, percentage_of_prime_rides, total_revenue, average_ride_revenue]
    c = ['Driver ID', 'Number of Rides', 'Average Ride Distance in Miles', 'Average Ride Duration in Minutes',
         'Percentage of Prime Rides: ', 'Total Revenue: ', 'Average Ride Revenue']
    profile = pd.DataFrame(values, index=c, columns=['Data'])
    return (profile)

def show_all_driver_profiles(): 
    for id in driver_ids['driver_id']:
        print(create_driver_profile(id))

# print(create_driver_profile('002be0ffdc997bd5c50703158b7c2491'))
show_all_driver_profiles()