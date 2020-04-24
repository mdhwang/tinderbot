# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime, timedelta

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

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

import base64

image_filename = 'images/tinderbot_logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())



################################################################################################
############ GATHER LATEST DATA ################################################################
################################################################################################


df = pd.read_csv('data/profile_data.csv')
df = clean(df)
stats(df)
df = fill_missing_cities(df)
df = add_location_values(df)
# map = plot_user_heatmap(df)
# map.save('heatmap.html')

################################################################################################
############ GENERATE PLOTS  ###################################################################
################################################################################################


################################################################################################
############ START DASH APP ####################################################################
################################################################################################

BootyStrap = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

app = dash.Dash(__name__, 
                external_stylesheets=[BootyStrap],
                meta_tags=[
                    {"name": "author", "content": "Matt Hwang"}
                ]
            )

app.title = 'Tinderbot'
server = app.server

# app.config['suppress_callback_exceptions'] = True # This is to prevent app crash when loading since we have plot that only render when user clicks.



app.layout = html.Div(style={'backgroundColor': '#fafbfd'},
    children=[
            # HEADER START

            html.Div(style={'marginRight': '1.5%',},
                id="header",
                children=[
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image)),

                    html.H1(
                        children="Tinderbot",
                        style={
                            'textAlign': 'center',
                    }),

                    html.H4(
                        children='Statistical insight based on worldwide Tinder profiles gathered by an automated bot',
                        style={
                            'textAlign': 'center',
                            }
                    ),

                    html.Hr(style={'marginTop': '.5%'},),

                    html.P(
                        id="description",
                        children=dcc.Markdown(
                        children=(
                            '''
                            On April 2nd (day after April Fool's Day lol), Tinder announced that it will open up the use
                            of it's Passport feature to all Tinder users.  The Passport feature allows you to match
                            with people all over the world versus your immediate area in an attempt to combat lonliness and boredom
                            during the shelter in place and quarantine directives being rolled out all over.

                            I decided to use this opportunity to gather Tinder profile information of users around the world to build
                            a database to apply my newfound Data Science and Analytical skills towards in an attempt to combat lonliness and boredom
                            during the shelter in place and quarantine directives being rolled out all over.

                            '''
                            )
                        ),
                        style={
                            'textAlign': 'center',
                            }
                    ),
                    
                    html.Hr(style={'marginTop': '.5%'},)
                    
                ]),

            html.Div(style={'textAlign': 'center'},
                children=[
                    html.Br(),
                    html.H3('Stay safe out in them streets.  Keep your distance and most importantly:'),
                    html.H2('Wash 👏 Your 👏 Hands 👏 '),
                    html.A('www.THWDesigns.com',href='https://thwdesigns.com'),
                ]),

            # FOOTER START
            html.Div(style={'textAlign': 'center'},
                children=[
                    html.Br(),
                    html.Br(),
                    html.Hr(),
                    html.P('Shout out to the below GitHub repos for inspiration.'),
                    html.A('Perishleaf Project', href='https://github.com/Perishleaf/data-visualisation-scripts/tree/master/dash-2019-coronavirus',target='_blank'),
                    html.Br(),
                    html.A('NYT Github',href='https://github.com/nytimes/covid-19-data'),
                ]),

])

if __name__ == '__main__':
    # change host from the default to '0.0.0.0' to make it publicly available
    app.server.run(port=8000, host='127.0.0.1')
    app.run_server(debug=True)