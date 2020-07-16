import pandas as pd
import nltk
from clean import *
from faces import *

import pickle

from PIL import Image
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

import wget

frontalface_default_path = "cascades/haarcascade_frontalface_default.xml"
frontalface_alt_path = "cascades/haarcascade_frontalface_alt.xml"
frontalface_alt2_path = "cascades/haarcascade_frontalface_alt2.xml"
profileface_path = "cascades/haarcascade_profileface.xml"


face_cascade = cv2.CascadeClassifier(frontalface_default_path)
facealt_cascade = cv2.CascadeClassifier(frontalface_alt_path)
facealt2_cascade = cv2.CascadeClassifier(frontalface_alt2_path)
profileface_cascasde = cv2.CascadeClassifier(profileface_path)

class User:
    def __init__(self, name, age, college, job, city, gender, distance, details, anthem, urls, faces ):
        self.name = name
        self.age = age
        self.college = college
        self.job = job
        self.city = city
        self.gender = gender
        self.distance = distance
        self.details = details
        self.anthem = anthem
        self.urls = urls
        self.faces = faces

df = pd.read_csv('data/raw/profile_data.csv')
df = clean(df)
df = fill_missing_cities(df)
df = add_location_values(df)

def find_face(img):
    img = Image.open(img).convert('RGB')
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facealt_cascade.detectMultiScale(gray, 1.1, 4)
    
    # print("Found {} faces".format(len(faces)))
    face_arr = []
    for(x , y,  w,  h) in faces:
        face_arr.append(gray[y:y+h,x:x+h])
    # for each in face_arr:
    #     cv2_imshow(each)
    return face_arr

users = []
for i in range(2320,2360):
    print("starting row {}".format(i))
    links = [x.strip('"').strip("'") for x in df.iloc[i,9]]
    faces = []
    for url in links:
        print(url)
        try:
            img = wget.download(url,out='data/images')
            print(img)
            found = find_face(img)
            if found:
                faces.append(found)
        except:
            print('Forbidden URL')
    if faces:
        users.append(User(df.iloc[i,0],
                      df.iloc[i,1],
                      df.iloc[i,2],
                      df.iloc[i,3],
                      df.iloc[i,4],
                      df.iloc[i,5],
                      df.iloc[i,6],
                      df.iloc[i,7],
                      df.iloc[i,8],
                      links,
                      faces))

pickle.dump(users, open( "users2.p", "wb" ))