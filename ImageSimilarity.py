import os, sys
sys.path.append("..")
import glob
import imageio
import tensorflow as tf
import keras, keras.layers as L, keras.backend as K
import numpy as np
from scipy.misc import imresize
from sklearn.model_selection import train_test_split
#%matplotlib inline
import matplotlib.pyplot as plt
import keras_utils #taken from course "Introduction to Deep Learning" on Coursera
import numpy as np
from keras_utils import reset_tf_session
import pickle

#Constants
IMG_SHAPE = (224, 224, 3)
CODE_SIZE = 64

#Get a list of paths to all images in a given directory and subdirectories
def get_image_paths(path=".", extensions=["jpg","jpeg","png","tga","bmp"]):
    result = []
    _ = [result.extend(glob.glob(os.path.join(path, '**/*.%s' % ext), recursive=True)) for ext in extensions]
    return result

#Load images in resized form
def load_images(paths):
    images = []
    for path in paths:
        images.append(imresize(imageio.imread(path, pilmode="RGB"), IMG_SHAPE, interp="bilinear"))
    return np.concatenate([aux[None,...] for aux in images], axis=0)

#Neural Networks
def build_pca_autoencoder(img_shape = IMG_SHAPE, code_size = CODE_SIZE):
    """
    Here we define a simple linear autoencoder.
    We also flatten and un-flatten data to be compatible with image shapes
    """
    
    encoder = keras.models.Sequential()
    encoder.add(L.InputLayer(img_shape))
    encoder.add(L.Flatten())                  #flatten image to vector
    encoder.add(L.Dense(code_size))           #actual encoder
    
    encoder.load_weights("encoder_pca.h5")
    
    return encoder

def build_deep_autoencoder(img_shape = IMG_SHAPE, code_size = CODE_SIZE):
    """PCA's deeper brother."""
    H,W,C = img_shape
    
    encoder = keras.models.Sequential()
    encoder.add(L.InputLayer(img_shape))
    encoder.add(L.Conv2D(filters=32, kernel_size=(3,3), padding="same", activation="elu"))
    encoder.add(L.MaxPooling2D(pool_size=(2,2)))
    encoder.add(L.Conv2D(filters=64, kernel_size=(3,3), padding="same", activation="elu"))
    encoder.add(L.MaxPooling2D(pool_size=(2,2)))
    encoder.add(L.Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="elu"))
    encoder.add(L.MaxPooling2D(pool_size=(2,2)))
    encoder.add(L.Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="elu"))
    encoder.add(L.MaxPooling2D(pool_size=(2,2)))
    encoder.add(L.Flatten())
    encoder.add(L.Dense(code_size))
    
    encoder.load_weights("encoder.h5")
    
    return encoder

def load_NN_weights(encoder, path):
    encoder.load_weights(path)

# Build code database, returns a dictionary of dictionaries containing image paths and the respective codes
def build_code_database(encoder, path="."):
    paths = get_image_paths(path)
    codes = {}
    i = 0
    for p in paths:
        codes[i]={'path':p, 'name':os.path.basename(p), 'code':encoder.predict(imresize(imageio.imread(p, pilmode="RGB"), IMG_SHAPE, interp="bilinear")[None])}
        i += 1
    return codes

def save_database(database, name, overwrite=False):
    if((os.path.isfile(name) and overwrite) or not os.path.isfile(name)):
        pickle.dump(database, open(name, "wb"))
    elif(os.path.isfile(name) and not overwrite):
        i = 1
        n, ext = os.path.split(name)
        while(os.path.isfile(n + i + ext)):
            i += 1
        pickle.dump(database, open(n + i + ext, "wb"))

def load_database(name):
    if(os.path.isfile(name)):
        return pickle.load(open(name, "rb"))

# Compare input image to database (using euclidean distance aka L2 norm of the codes)
def l2_norm(v, u):
    return np.linalg.norm(v - u)

def similarity_search(inp_path, database, encoder, max_dist=0):
    code = encoder.predict(imresize(imageio.imread(inp_path, pilmode="RGB"), IMG_SHAPE, interp="bilinear")[None])
    hits = []
    for d in database.values():
        dist = l2_norm(code, d['code'])
        if dist <= max_dist:
            d['distance'] = dist
            hits.append(d)
    return hits