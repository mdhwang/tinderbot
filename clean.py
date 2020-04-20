import pandas as pd
import math as math

def clean(data):
    '''
    Remove any missing data
    Remove duplicates
    Convert to correct data types
    Parse Strings
    Return dataframe
    '''
    print("CLEANING DATA")
    print("...")
    print("FOUND {} ENTRIES".format(len(data)))
    empty_entries = data.name.isna()
    data = data[-empty_entries]
    print("REMOVED {} EMPTY ENTRIES".format(empty_entries.sum()))
    duplicated_entries = data.duplicated()
    data = data[-duplicated_entries]
    print("REMOVED {} DUPLICATED ENTRIES".format(duplicated_entries.sum()))
    
    # Data conversions to be added into webscraping script
    data.name = data.name.apply(lambda x: x.capitalize())
    data.age = data.age.apply(lambda x: int(x) if not math.isnan(x) else x)
    data.city = data.city.apply(lambda x: x[9:] if type(x) != float else x)
    data.distance = data.distance.apply(lambda x: x.split(' ')[0] if type(x) != float else x)

    
    return data

def stats(data):
    print("CALCULATING STATS")
    print("...")
    total = len(data)
    print("FOUND {} ENTRIES".format(total))
    num_age = total - data.age.isna().sum()
    print("{} ENTRIES HAVE AGE DATA ({}%)".format(num_age,round(100*num_age/total,1)))
    num_college = total - data.college.isna().sum()
    print("{} ENTRIES HAVE COLLEGE DATA ({}%)".format(num_college,round(100*num_college/total,1)))
    num_city = total - data.city.isna().sum()
    print("{} ENTRIES HAVE CITY DATA ({}%)".format(num_city,round(100*num_city/total,1)))
    num_jobs = total - data.job.isna().sum()
    print("{} ENTRIES HAVE JOB DATA ({}%)".format(num_jobs,round(100*num_jobs/total,1)))
    num_gender = total - data.gender.isna().sum()
    print("{} ENTRIES HAVE GENDER DATA ({}%)".format(num_gender,round(100*num_gender/total,1)))
    num_distance = total - data.distance.isna().sum()
    print("{} ENTRIES HAVE DISTANCE DATA ({}%)".format(num_distance,round(100*num_distance/total,1)))
    num_details = total - data.details.isna().sum()
    print("{} ENTRIES HAVE DETAIL DATA ({}%)".format(num_details,round(100*num_details/total,1)))
    num_anthem = total - data.anthem.isna().sum()
    print("{} ENTRIES HAVE ANTHEM DATA ({}%)".format(num_anthem,round(100*num_anthem/total,1)))
    print("----")
    avg_age = data.age.mean()
    print("AVERAGE AGE IN DATA SET: {}".format(int(avg_age)))
    unique_college = len(data.college.unique())
    print("NUMBER OF UNIQUE COLLEGES: {}".format(unique_college))
    unique_jobs = len(data.job.unique())
    print("NUMBER OF UNIQUE JOBS: {}".format(unique_jobs))
    unique_cities = len(data.city.unique())
    print("NUMBER OF UNIQUE CITIES: {}".format(unique_cities))
        

# df = pd.read_csv('data/profile_data.csv')
# print(df.head())
# print("------------------------")
# cleaned = clean(df)
# print(cleaned.head())