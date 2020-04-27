import pandas as pd

from topics import *

from clean import stats

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
    citydf['college'] = reduced.groupby('city').apply(lambda x: round(100*x['college'].count()/x['name'].count(),1))
    citydf['job'] = reduced.groupby('city').apply(lambda x: round(100*x['job'].count()/x['name'].count(),1))
    citydf['anthem'] = reduced.groupby('city').apply(lambda x: round(100*x['anthem'].count()/x['name'].count(),2))
    citydf['age_dist'] = reduced.groupby('city').apply(lambda x: x['age'].to_list())
    for each in topics:
        citydf[each] = reduced.groupby('city').apply(lambda x: round(100*x[each].sum()/x['name'].count(),2))

    return citydf

def top_5(citydf):
    print("---------------------------------------------")
    print("-----------HERE ARE YOUR TOP 5---------------")
    print("-----TOP 5 CITIES WITH MOST DATA ENTRIES-----")
    print(citydf.DPs.sort_values(ascending=False).head())
    print("-----TOP 5 CITIES WITH HIGHEST COLLEGE %-----")
    print(citydf.college.sort_values(ascending=False).head())
    print("---------------------------------------------")
    print("-------TOP 5 CITIES WITH HIGHEST JOB %-------")
    print(citydf.job.sort_values(ascending=False).head())
    print("------TOP 5 CITIES WITH HIGHEST ANTHEM %-----")
    print(citydf.anthem.sort_values(ascending=False).head())
    print("--------TOP 5 CITIES WITH HIGHEST IG %-------")
    print(citydf.instagram.sort_values(ascending=False).head())
    print("-------TOP 5 CITIES WITH HIGHEST SNAP %------")
    print(citydf.snapchat.sort_values(ascending=False).head())
    print("-------TOP 5 CITIES WITH HIGHEST COVID %-----")
    print(citydf.covid19.sort_values(ascending=False).head())
    print("-------TOP 5 CITIES WITH HIGHEST WEED %-----")
    print(citydf.cannabis.sort_values(ascending=False).head())
    print("---------------------------------------------")
    print(citydf.head())

df = pd.read_csv("data/processed/cleaned_data.csv")
new = calc_city_stats(df)
top_5(new)

