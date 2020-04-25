import csv
import json
import pandas as pd

from opencage.geocoder import OpenCageGeocode

with open('data/loc_data.json','r') as file:
    location_dict = json.load(file)

def append_data():
    '''
    Try to append any new data into raw data file if file found
    '''
    print("-----------------")
    print("PROCESS START")
    print("LOOKING FOR NEW RAW DATA TO APPEND TO MASTER")
    try:
        with open("append/profile_data.csv",'r') as append_file:
            reader = csv.reader(append_file)
            next(reader)
            print("FOUND NEW RAW DATA - ATTEMPTING TO APPEND TO MASTER")
        try:
            with open('raw/profile_data.csv','a') as file:
                writer = csv.writer(file)
                with open("append/profile_data.csv",'r') as append_file:
                    reader = csv.reader(append_file)
                    next(reader)
                    for row in reader:
                        writer.writerow(row)
                    append_file.close()
                file.close()
            print("NEW DATA APPENDED TO MASTER")
        except:
            print("COULD NOT APPEND NEW DATA TO MASTER")
    except:
        print("COULD NOT FIND NEW DATA")
    print("SCRIPT COMPLETED")
    print("-----------------")

def update_location_dictionary(data):
    '''
    Identify cities that are not in the location data dictionary
    Use OpenCageGeocode to find location info
    Append location data dictionary
    '''
    data.city = data.city.apply(lambda x: x[9:] if type(x) != float else x)
    new = data[-data.city.isna()]
    cities = new.city.unique().tolist()
    still_need = []
    locations = list(location_dict)
    for each in cities:
        if each not in locations:
            still_need.append(each)
    key = "94b38715f5b64f4db83c6313faf5893e"
    geocoder = OpenCageGeocode(key)
    location_cache = {}
    for each in still_need:
        try:
            location_cache[each] = geocoder.geocode(each)[0]['geometry']
            location_cache[each]['country'] = geocoder.geocode(each)[0]['components']['country']
            if location_cache[each]['country'] == "United States of America":
                location_cache[each]['state'] = geocoder.geocode(each)[each][0]['components']['state']
        except:
            pass
    with open("loc_data.json", "r+") as file:
        info = json.load(file)
        info.update(location_cache)
        file.seek(0)
        json.dump(info, file)
