import pandas as pd
import math as math
import json
import numpy as np

from clean import *
from append_data import *

with open('data/loc_data.json','r') as file:
    location_dict = json.load(file)

print("-----------------")
print("STARTING PROGRAM")
query = input("NEED TO INPUT NEW DATA? Y/N : ")
if query.lower() == 'y':
    print("-----------------")
    print("THIS SCRIPT WILL APPEND NEW DATA TO MASTER RAW FILE")
    print("MAKE SURE TO PUT NEW DATA INTO APPEND FOLDER")
    runit = input("Run Script? Y/N ? : ")
    if runit.lower() == 'y':
        append_data()
    else:
        print("SCRIPT CANCELLED - NO DATA ADDED")
        print("SCRIPT COMPLETED")
        print("-----------------")
else:
    print("USING EXISTING DATA FROM RAW FOLDER")

print("-----------------")
query = input("NEED TO UPDATE DICTIONARY? Y/N : ")
if query.lower() == 'y':
    df = pd.read_csv("data/raw/profile_data.csv")
    update_location_dictionary(df)
    # Reload updated cache file
    with open('data/loc_data.json','r') as file:
        location_dict = json.load(file)
else:
    print("USING EXISTING LOCATION CACHE DATA")
      

print("-----------------")
query = input("RUN DATA CLEANING SCRIPT? Y/N : ")
if query.lower() == 'y':
    df = pd.read_csv('data/raw/profile_data.csv')
    df = clean(df)
    df.to_csv('data/processed/cleaned_data.csv',index=False)
    print("-----------------")
    print("RAW DATA CLEANED AND SAVED IN PROCESSED FOLDER")
    print("-----------------")
    stats(df)