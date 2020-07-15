import pandas as pd
from PIL import Image
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

frontalface_default_path = "cascades/haarcascade_frontalface_default.xml"
frontalface_alt_path = "cascades/haarcascade_frontalface_alt.xml"
frontalface_alt2_path = "cascades/haarcascade_frontalface_alt2.xml"
profileface_path = "cascades/haarcascade_profileface.xml"


face_cascade = cv2.CascadeClassifier(frontalface_default_path)
facealt_cascade = cv2.CascadeClassifier(frontalface_alt_path)
facealt2_cascade = cv2.CascadeClassifier(frontalface_alt2_path)
profileface_cascasde = cv2.CascadeClassifier(profileface_path)

def find_face(img_path):
    if img_path[-4:] == 'webp':
        img = Image.open(img_path).convert('RGB')
    else:
        img = cv2.imread(img_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facealt_cascade.detectMultiScale(gray, 1.1, 4)
    
    face_arr = []
    for(x , y,  w,  h) in faces:
        face_arr.append(gray[y:y+h,x:x+h])
    
    for each in face_arr:
        cv2_imshow(each)

# find_face('data/testfaces/sc/1.jpg')