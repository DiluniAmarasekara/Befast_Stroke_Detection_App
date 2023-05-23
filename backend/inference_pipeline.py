import os
import cv2
import tensorflow as tf
import numpy as np
from typing import List
import imageio
import matplotlib.pyplot as plt
import glob
from tqdm import tqdm
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Conv3D, LSTM, Dense, Dropout, Bidirectional, MaxPool3D, Activation, Reshape, SpatialDropout3D, BatchNormalization, TimeDistributed, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping
from tensorflow.keras.optimizers import legacy

vocab = [x for x in "abcdefghijklmnopqrstuvwxyz'?!123456789 "]
char_to_num = tf.keras.layers.StringLookup(vocabulary=vocab, oov_token="")
num_to_char = tf.keras.layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True
)

def get_model():
    model = Sequential()
    model.add(Conv3D(128, 3, input_shape=(75,46,140,1), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPool3D((1,2,2)))

    model.add(Conv3D(256, 3, padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPool3D((1,2,2)))

    model.add(Conv3D(75, 3, padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPool3D((1,2,2)))

    model.add(TimeDistributed(Flatten()))

    model.add(Bidirectional(LSTM(128, kernel_initializer='Orthogonal', return_sequences=True)))
    model.add(Dropout(.5))

    model.add(Bidirectional(LSTM(128, kernel_initializer='Orthogonal', return_sequences=True)))
    model.add(Dropout(.5))

    model.add(Dense(char_to_num.vocabulary_size()+1, kernel_initializer='he_normal', activation='softmax'))
    return model

model = get_model()

def CTCLoss(y_true, y_pred):
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

    loss = tf.keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)
    return loss

model.compile(optimizer=legacy.Adam(learning_rate=0.0001), loss=CTCLoss)
# Load best weights
model.load_weights('models/checkpoint')

def load_video(path:str) -> List[float]: 

    cap = cv2.VideoCapture(path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = tf.image.rgb_to_grayscale(frame)
        frames.append(frame[190:236,80:220,:])
    cap.release()
    
    mean = tf.math.reduce_mean(frames)
    std = tf.math.reduce_std(tf.cast(frames, tf.float32))
    return (tf.cast(frames, tf.float32) - tf.cast(mean, tf.float32)) / std

def load_data(path: str): 
    print("Path is",path, flush=True)
    path = bytes.decode(path.numpy())
    video_path = path
    # file_name = path.split('//')[-1].split('.')[0]
    # File name splitting for windows
#     file_name = path.split('/')[-1].split('.')[0]
    alignment_path = ""
    frames = load_video(video_path) 
    alignments = tf.zeros(5, dtype=tf.int64)
    
    return frames, alignments

def mappable_function(path:str) ->List[str]:
    result = tf.py_function(load_data, [path], (tf.float32, tf.int64))
    return result

def decode_to_text(inp_arr):
    decoded_arr = []
    
    for ele in inp_arr:
#         tf string is eager tensor
        tf_string = tf.strings.reduce_join([num_to_char(word) for word in ele])
#     Convert eager tensor to numpy first., then you get bytes not a string,then you have to decode the bytes to convert it to a python string
        decoded_arr.append(str(tf_string.numpy().decode('utf-8')))
        
    if len(decoded_arr) == 1:
        return decoded_arr[0]
    return decoded_arr

def get_predictions(data):
    predicted_text_arr = []
    
    pred = model.predict(data)
    for data_slice in pred:
#         np.newaxis adds a new axis to the data slice such that it is comptible with the model imput dimensions
        decoded = tf.keras.backend.ctc_decode(data_slice[np.newaxis,...], input_length=[75], greedy=True)[0][0].numpy()
        text_output = decode_to_text(decoded)
        predicted_text_arr.append(text_output)
    
    return predicted_text_arr


def inference_pipeline(path):
    data = tf.data.Dataset.list_files(path)
    data = data.map(mappable_function)
    data = data.padded_batch(2, padded_shapes=([75,None,None,None],[40]))
    data = data.prefetch(tf.data.AUTOTUNE)
    
    test = data.take(1)
    pred = get_predictions(next(test.as_numpy_iterator())[0])
    return pred[0]

if __name__ == '__main__':
    path = "C://Users//DELL//OneDrive//Documents//Projects//BEFAST//Befast_Stroke_Detection_App//data//s1//bbaf2n.mpg"
    pred = inference_pipeline(path)
    print(pred)