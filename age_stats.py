import pandas as pd

from topics import *

from clean import stats

def calc_age_stats(df):
    '''
    Take in cleaned and processed data, remove cities with less than 50 data points
    Calculate statistics per city - display top 5
    - % that advertise IG
    - % that advertise SC
    - % that mention Coivd
    - % 

    '''
    reduced = df.groupby('age').filter(lambda x: x["name"].count() > 2000)
    citydf = pd.DataFrame(reduced.groupby('age').size(),columns=["DPs"])
    citydf['college'] = reduced.groupby('age').apply(lambda x: round(100*x['college'].count()/x['name'].count(),1))
    citydf['job'] = reduced.groupby('age').apply(lambda x: round(100*x['job'].count()/x['name'].count(),1))
    citydf['anthem'] = reduced.groupby('age').apply(lambda x: round(100*x['anthem'].count()/x['name'].count(),2))
    citydf['city'] = reduced.groupby('age').apply(lambda x: round(100*x['city'].count()/x['name'].count(),2))
    # citydf['age_dist'] = reduced.groupby('age').apply(lambda x: x['age'].to_list())
    for each in topics:
        citydf[each] = reduced.groupby('age').apply(lambda x: round(100*x[each].sum()/x['name'].count(),2))

    return citydf

def top_5(citydf):
    print("---------------------------------------------")
    print("-----------HERE ARE YOUR TOP 8---------------")
    print("-----TOP 8 CITIES WITH MOST DATA ENTRIES-----")
    print(citydf.DPs.sort_values(ascending=False).head(8))
    print("-----TOP 8 CITIES WITH MOST CITIES-----")
    print(citydf.city.sort_values(ascending=False).head(8))
    print("-----TOP 8 CITIES WITH HIGHEST COLLEGE %-----")
    print(citydf.college.sort_values(ascending=False).head(8))
    print("-------TOP 8 CITIES WITH HIGHEST JOB %-------")
    print(citydf.job.sort_values(ascending=False).head(8))
    print("------TOP 8 CITIES WITH HIGHEST ANTHEM %-----")
    print(citydf.anthem.sort_values(ascending=False).head(8))
    print("--------TOP 8 CITIES WITH HIGHEST IG %-------")
    print(citydf.instagram.sort_values(ascending=False).head(8))
    print("-------TOP 8 CITIES WITH HIGHEST SNAP %------")
    print(citydf.snapchat.sort_values(ascending=False).head(8))
    print("-------TOP 8 CITIES WITH HIGHEST COVID %-----")
    print(citydf.covid19.sort_values(ascending=False).head(8))
    print("-------TOP 8 CITIES WITH HIGHEST WEED %-----")
    print(citydf.cannabis.sort_values(ascending=False).head(8))
    print("-------TOP 8 CITIES WITH HIGHEST ALCOHOL %-----")
    print(citydf.alcohol.sort_values(ascending=False).head(8))
    print("-------TOP 8 CITIES WITH HIGHEST TV %-----")
    print(citydf.tv.sort_values(ascending=False).head(8))
    print("-------TOP 8 CITIES WITH HIGHEST Premium Snap %-----")
    print(citydf.premium.sort_values(ascending=False).head(8))
    print("-------TOP 8 CITIES WITH HIGHEST OFFICE %-----")
    print(citydf.office.sort_values(ascending=False).head(8))
    print("---------------------------------------------")
    print(citydf.head())

df = pd.read_csv("data/processed/cleaned_data.csv")
new = calc_age_stats(df)
top_5(new)

