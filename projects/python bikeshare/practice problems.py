import pandas as pd

filename = 'chicago.csv'

# load data file into a dataframe
df = pd.read_csv(filename)
#print(df)
# print(df.columns)
# print(df.index)
# print(df.size)
# print(df.ndim)

# convert the Start Time column to datetime
print(df['Start Time'])
df['Start Time'] = pd.to_datetime(df['Start Time'])
print(df['Start Time'])

# extract hour from the Start Time column to create an hour column
#df['hour'] =

# find the most common hour (from 0 to 23)
#popular_hour =

#print('Most Frequent Start Hour:', popular_hour)
