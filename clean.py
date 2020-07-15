import pandas as pd
import numpy as np
import json

from sklearn.neighbors import KNeighborsClassifier

from emoji import UNICODE_EMOJI

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

stop_words = set(stopwords.words('english')) 
bad_chars = ["\n","\r",'\'','"',',','.','(',')','&','!','?',':','-','`','...','..','/']
for each in bad_chars:
    stop_words.add(each)

from topics import *


with open('data/loc_data.json','r') as file:
    location_dict = json.load(file)

def clean(data):
    '''
    Remove any missing data
    Remove duplicates
    Convert to correct data types
    Parse Strings
    Return dataframe
    '''
    print("-----------------")
    print("CLEANING DATA")
    print("...")
    print("FOUND {} ENTRIES".format(len(data)))
    empty_entries = data.name.isna()
    data = data[-empty_entries]
    print("REMOVED {} EMPTY ENTRIES".format(empty_entries.sum()))
    duplicated_entries = data.duplicated()
    data = data[-duplicated_entries]
    print("REMOVED {} DUPLICATED ENTRIES".format(duplicated_entries.sum()))
    print("{} ENTRIES REMAIN".format(len(data)))
    
    # Data conversions to be added into webscraping script
    data.name = data.name.apply(lambda x: x.capitalize())
    data.age = data.age.apply(lambda x: int(x) if not np.isnan(x) else x)
    data.city = data.city.apply(lambda x: x[9:] if type(x) != float else x)
    data.distance = data.distance.apply(lambda x: int(x.split(' ')[0]) if type(x) != float else x)
    data.profile_pic_urls = data.profile_pic_urls.apply(lambda x: x.strip("[]").split(", "))
    data['num_pics'] = data.profile_pic_urls.apply(lambda x: len(x))
    data['filtered_details'] = data[-data.details.isna()].details.apply(lambda x: filter_details(x))
    
    
    return data

def filter_details(text):
    word_tokens = word_tokenize(text.lower())
    word_tokens = set(word_tokens)
    filtered = word_tokens - stop_words
    return filtered

def stats(data):
    print("-----------------")
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
    print("...")
    avg_age = data.age.mean()
    print("AVERAGE AGE IN DATA SET: {}".format(int(avg_age)))
    unique_college = len(data.college.unique())
    print("NUMBER OF UNIQUE COLLEGES: {}".format(unique_college))
    unique_jobs = len(data.job.unique())
    print("NUMBER OF UNIQUE JOBS: {}".format(unique_jobs))
    unique_cities = len(data.city.unique())
    print("NUMBER OF UNIQUE CITIES: {}".format(unique_cities))
    avg_pics = data.num_pics.mean()
    print("AVERAGE PICS PER PROFILE: {}".format(int(avg_pics)))

        

def find_country(city):
    try:
        if type(city) != float:
            return location_dict[city]['country']
        else:
            return np.nan
    except:
        return np.nan

def find_state(city):
    try:
        if type(city) != float:
            return location_dict[city]['state']
        else:
            return np.nan
    except:
        return np.nan


def fill_city(series,city_list,KNN_model):
    if type(series.city)==float and ~np.isnan(series.distance):
        try:
            city = np.random.choice(city_list[series.distance],1, replace=True)[0]
        except:
            if ~np.isnan(series.distance):
                city = KNN_model.predict(np.array([[series.distance]]))[0]
            else:
                city = np.nan
    else:
        city = series.city
    return city

def fill_missing_cities(data):
    '''
    Use Numpy Random Choice to fill in missing cities based on others in same distance
    Use KNN for distances that are not explicitly specified
    '''
    print("-----------------")
    print("FILLING MISSING CITY VALUES")
    num = data.city.isna().sum()
    print("FOUND {} MISSING VALUES".format(num))
    filtered = data[-data.city.isna()].copy()
    filtered = filtered[-filtered.distance.isna()]
    city_list = {}
    for each in filtered.distance.unique():
        city_list[each] = list(filtered[filtered.distance == each].city)

    #KNN for remaining values:
    X = np.array(list(filtered.distance)).reshape(-1,1)
    y = np.array(list(filtered.city))
    KNN_City = KNeighborsClassifier(n_neighbors=10).fit(X,y)
    
    data.city = data.apply(lambda x: fill_city(x,city_list,KNN_City), axis =1)
    new_num = data.city.isna().sum()
    print("{} MISSING CITY VALUES REMAIN ({}%)".format(new_num,round(new_num/len(data),2)))
    
    return data

def find_coordinates(city):
    '''
    Find latitude/longitude values from dict, if not look up, fill value and update master dictionary.
    '''
    try:
        return (location_dict[city]['lat'],location_dict[city]['lng'])
    except:
        return np.nan

def add_location_values(data):
    '''
    Add in lat and longitude values
    '''
    print("-----------------")
    print("ADDING LOCATION COORDINATE VALUES")
    data['location'] = data.city.apply(lambda x: find_coordinates(x))
    data['country'] = data.city.apply(lambda x: find_country(x))
    data['state'] = data[data.country=="United States of America"].city.apply(lambda x: find_state(x))
    num = data.location.isna().sum()
    print("COULD NOT FIND LOCATION DATA FOR {} ENTRIES ({}%)".format(num,round(num/len(data),2)))
    return data
   
def topic_check(filtered_details,topic):
    if filtered_details.intersection(topics[topic]) != set():
        return True
    return False

def second_check(filtered_details,existing,topic):
    if existing == True:
        return True
    for word in list(filtered_details):
        for each in second_pass[topic]:
            if each in word:
                return True
    return False

def add_topics(data):
    for each in topics:
        data[each] = data[-data.filtered_details.isna()].filtered_details.apply(lambda x: topic_check(x,each))
    
    for each in second_pass:
        data[each] = data[-data.filtered_details.isna()].apply(lambda x: second_check(x.filtered_details,x[each],each),axis=1)
    return data


