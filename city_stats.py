import pandas as pd

from topics import *

def calc_city_stats(df):
    '''
    Take in cleaned and processed data, remove cities with less than 100 data points
    Calculate statistics per city - display top 5
    - % that advertise IG
    - % that advertise SC
    - % that mention Coivd
    - % 

    '''
    reduced = df.groupby('city').filter(lambda x: x["name"].count() > 50)
    citydf = pd.DataFrame(reduced.groupby('city').size(),columns=["DPs"])
    citydf['college'] = reduced.groupby('city').apply(lambda x: x['college'].sum()/x['name'].count())
    citydf['job'] = reduced.groupby('city').apply(lambda x: x['job'].sum()/x['name'].count())
    citydf['anthem'] = reduced.groupby('city').apply(lambda x: x['anthem'].sum()/x['name'].count())
    citydf['age_dist'] = reduced.groupby('city').apply(lambda x: x['age'].to_list())
    for each in topics:
        citydf[each] = reduced.groupby('city').apply(lambda x: x[each].sum()/x['name'].count())

    return citydf

df = pd.read_csv("data/processed/cleaned_data.csv")
new = calc_city_stats(df)
print(new.head())