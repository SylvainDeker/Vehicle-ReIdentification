from __future__ import absolute_import, division, print_function, unicode_literals

import gc
import os
import requests
import zipfile
import cv2
import random
import keras
from keras import backend
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential, model_from_json
from keras.models import Model
from keras.layers import Dense, Activation, Dropout, Flatten, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.utils import np_utils
from keras import backend as K
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.preprocessing import image

from keras.applications.inception_v3 import InceptionV3,preprocess_input,decode_predictions

from keras.models import load_model

import numpy as np
import matplotlib.pyplot as plt

from keras import applications
from keras.utils import np_utils

from tqdm import tqdm_notebook as tqdm

from scipy.spatial import distance

def initModel():
  inception_model = load_model("./model.hdf5")
  inception_model.load_weights("./weight.hdf5")
  featureExtractor = Model(inputs=inception_model.input, outputs=inception_model.layers[-2].output)
  return(featureExtractor)

def getSemantic(imageName):
  return(np.loadtxt(imageName))

def saveSemantic(imageName,features):
  np.savetxt(imageName,features)

def prepareSemanticDataSet(featureExtractor):
  for file in os.listdir("./VeRi_with_plate/image_train/"):
    img = image.load_img(file, target_size=(IMG_HEIGHT, IMG_WIDTH))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = featureExtractor.predict(x)
    saveSemantic('./semanticFolder/'+file,features)

def googleNetScore(img_path,featureExtractor):
  semanticScore = []
  name = []
  img = image.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  features = featureExtractor.predict(x)

  for file in os.listdir("./semanticFolder/"):
    semanticScore = semanticScore.append(distance.euclidean(features,getSemantic(file)))
    name = name.append(file)
  newListe = list(zip(semanticScore, name))
  return(newListe)

#featureExtractor = load_model("./featureExtractor_model.hdf5")
#featureExtractor.load_weights("./featureExtractor_weight.hdf5")
