import pandas as pd 
import matplotlib.pyplot as plt 
from collections import Counter
from math import log10

# data source https://github.com/CSSEGISandData/COVID-19
path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

# create a dataframe for cumulative cases updated daily
file_cases = 'time_series_covid19_confirmed_global.csv'
df_cases = pd.read_csv(path + file_cases)

# drop latitude and longitude
df_cases.drop(['Lat', 'Long'], axis=1, inplace=True)
# group by country (some countries have state data split out)
df_cases_grp = df_cases.groupby(['Country/Region']).sum()

# Select country
country = 'South Africa'

# set up the dataframe
country_data = pd.DataFrame()
country_data['Date'] = df_cases_grp.loc[country, '1/22/20':].index
country_data['Cases'] = df_cases_grp.loc[country, '1/22/20':].values
country_data['New'] = country_data['Cases'] - country_data['Cases'].shift(1)

print (country_data)

# graph the daily cases (excluding x axis labels)
plt.bar(country_data['Date'], country_data['New'])
plt.title('{} (daily cases)'.format(country))
plt.xticks([])
plt.show()

# keep track of list of first digits
digits = []

# loop through all daily cases and extract first digit (skip first row NaN)
for amount in country_data['New'][1:]:
	first_digit = int(str(amount)[0])
	digits.append(first_digit)

# setup dataframe with first digit frequency and Benford expected frequency
df_digit = pd.DataFrame()
df_digit['Number'] = [digit for digit in range(1,10)]
df_digit['Count'] = [Counter(digits)[number] for number in df_digit['Number']]
df_digit['Frequency'] = [float(count) / (df_digit['Count'].sum()) for count in df_digit['Count']]
df_digit['Benford'] = [log10(1 + 1 / float(d)) for d in range(1,10)]

print (df_digit)

# graph the actual digit frequency
plt.bar(df_digit['Number'], df_digit['Frequency'], label='Actual')
# graph the Benford digit frequency (marker 'o' line '-' colour 'r')
plt.plot(df_digit['Number'], df_digit['Benford'], 'o-r', label='Benford')

plt.title('{} (daily cases: 1st digit distribution)'.format(country))
plt.legend(loc="upper right")
plt.xticks([1,2,3,4,5,6,7,8,9])	# show all x ticks
plt.show()
