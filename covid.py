# Hello World program in Python
import json
import urllib.request  # the lib that handles the url stuff
import pandas
from datetime import datetime, timedelta
import dateutil

pandas.options.display.float_format = '{:,.0f}'.format

url = "https://api.covidtracking.com/v1/us/current.json"
url = "https://api.covidtracking.com/v1/states/current.json"
url = "https://api.covidtracking.com/v1/states/daily.json"

#the_str = urllib.request.urlopen(url) 
#df = pandas.read_json(the_str)
#df.to_json("covid_save.json")
df = pandas.read_json("covid_save.json")

#print(df)


states = ["AL","CT","FL","IL","NY","VA", "NJ"]
populations = { # per https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population
    "AL": 4903185,
    "CT": 3565287,
    "FL": 21477737,
    "IL": 12671821,
    "NY": 19453561,
    "VA": 8535519,
    "NJ": 9241900
}
mask_usage = { # as of 10/27/2020
    "AL": .64,
    "CT": .70,
    "FL": .65,
    "IL": .67,
    "NY": .75,
    "VA": .68
}
cols = ["date","state","death","positive","dataQualityGrade"]

end_date = dateutil.parser.parse("12/23/2020") #datetime.now()
start_date = end_date - timedelta(days=30)
#print(now.strftime(f"%Y%m%d")+"-"+then.strftime(f"%Y%m%d"))

#today = 20201001
#print(today)
dates = [end_date.strftime(f"%Y%m%d"),start_date.strftime(f"%Y%m%d")]
print(dates)

df2 = df[df.state.isin(states)][df.date.isin(dates)][cols]
#print(df2)

#print(df2['death'].diff(periods=(len(states)*-1)))
df2['delta_d'] = df2['death'].diff(periods=(len(states)*-1))
df2['delta_p'] = df2['positive'].diff(periods=(len(states)*-1))
df2 = df2[df.date.isin([dates[0]])]
df2['case_mortality'] = df2['delta_d'] / df2['delta_p']
df2['population'] = df2['state'].map(populations)
df2['cases/100k'] = df2['delta_p'] / df2['population'] * 100000
df2['deaths/100k'] = df2['delta_d'] / df2['population'] * 100000
df2['deaths/100k per year'] = df2['deaths/100k'] * 12

#print(df2.transpose())
formatters2 = {
    'case_mortality':'{:.2%}'.format,
    'cases/100k':'{:.2f}'.format,
    'deaths/100k':'{:.2f}'.format,
    'deaths/100k per year':'{:,.2f}'.format,
    'population':lambda x : '{:,.1f}'.format(x/1000000)+'m'
    }
df2 = df2.drop(labels=['date','dataQualityGrade'],axis=1)
df2 = df2.rename(columns=
    {'death':'total deaths',
    'positive':'total positive',
    'delta_d':'death delta',
    'delta_p':'positive delta',
    })
#df2.style.format(formatters2)
for key, value in formatters2.items():
    df2[key] = df2[key].apply(formatters2[key])
#print(df2.to_string(formatters=formatters2, float_format='{:,.0f}'.format))
print(df2.transpose())

flu_mortality = 17.1 # per 100k per https://www.cdc.gov/nchs/data/nvsr/nvsr68/nvsr68_09-508.pdf (row 8 on page 6) = 0.0171% 
# If mortality is ~2% of cases, then case risk of 0.855%.


# libraries
import matplotlib.pyplot as plt
import numpy as np
 
# create data
values=np.cumsum(np.random.randn(1000,1))
 
# use the plot function
plt.plot(values)
