import pandas as pd
from matplotlib import  pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)


def make_graph_one():
    data = pd.read_csv('CompleteFinalCalculatedData.csv')

    filtered = pd.DataFrame()


    filtered['Avg Ride Rev'] = data['Average Ride Revenue']
    filtered['% Prime Rides'] = data['Percentage of Prime Rides: ']


    filtered = filtered.set_index(filtered['Avg Ride Rev'], drop=True)

    print(filtered)

    filtered.plot.scatter(y='Avg Ride Rev', x='% Prime Rides')

    plt.show()


data = pd.read_csv('CompleteFinalCalculatedData.csv')
print(data)




