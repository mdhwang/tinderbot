import pandas as pd
import math as math
import json

import folium
from folium.plugins import HeatMap
import numpy as np

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="My_App")

from sklearn.neighbors import KNeighborsClassifier

with open('loc_data.json','r') as file:
    location_dict = json.load(file)

from clean import *

df = pd.read_csv('data/profile_data.csv')
df = clean(df)
stats(df)
df = fill_missing_cities(df)
df = add_location_values(df)
map = plot_user_heatmap(df)
map.save('heatmap.html')