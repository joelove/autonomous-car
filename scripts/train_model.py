import os
import sys
import cv2
import glob
import json
import numpy as np
import random

from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Input, Cropping3D, Convolution2D, MaxPooling3D, BatchNormalization, Dropout, Flatten, Dense

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
root_dir = os.path.join(script_dir, os.pardir)

sys.path.append(root_dir)

import config

def save_model(model):
    with open("model.json", "w") as json_file:
        json_file.write(model.to_json())

    model.save_weights("model.h5")


def create_model():
    image_shape = tuple(reversed(config.CAMERA_RESOLUTION))
    image_input = Input(shape=(*image_shape, 1))

    x = image_input
    x = BatchNormalization()(x)
    x = Convolution2D(8, (3, 3), strides=(2, 2), activation='relu')(x)
    x = BatchNormalization()(x)
    x = Convolution2D(16, (3, 3), strides=(2, 2), activation='relu')(x)
    x = BatchNormalization()(x)
    x = Convolution2D(32, (3, 3), strides=(2, 2), activation='relu')(x)
    x = BatchNormalization()(x)
    x = Convolution2D(64, (3, 3), strides=(2, 2), activation='relu')(x)
    x = BatchNormalization()(x)
    x = Convolution2D(64, (3, 3), strides=(2, 2), activation='relu')(x)
    x = Flatten(name='flattened')(x)
    x = BatchNormalization()(x)
    x = Dense(128, activation='relu')(x)

    angle_output = Dense(1, activation='tanh', name='angle_output')(x)
    throttle_output = Dense(1, activation='sigmoid', name='throttle_output')(x)

    model = Model(inputs=[image_input], outputs=[angle_output, throttle_output])
    model.compile(optimizer=Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-5, decay=0.0, amsgrad=False),
                  loss={'angle_output':'mean_absolute_error', 'throttle_output': 'mean_absolute_error'},
                  loss_weights={'angle_output': 0.9, 'throttle_output': 0.01})

    return model


def train_model():
    data_dir = os.path.join(root_dir, config.DATA_PATH)
    record_files = glob.glob(f'{data_dir}/*.json')

    total_records = len(record_files)
    image_shape = tuple(reversed(config.CAMERA_RESOLUTION))

    frames = np.empty((total_records, *image_shape, 1))
    angles = np.empty(total_records)
    throttles = np.empty(total_records)

    for index, filepath in enumerate(record_files):
        completion_ratio = float(index) / total_records
        percent_complete = int(round(completion_ratio * 100))

        print(f'Processing record {index} of {total_records}... ({percent_complete}%)', end="\r")

        with open(filepath) as record_file:
            record = json.load(record_file)

            angle = record["angle"]
            throttle = record["throttle"]

            angles[index] = angle
            throttles[index] = throttle

            frame_filename = record["frame_filename"]

            frame_array = cv2.imread(f'{config.DATA_PATH}/{frame_filename}')
            frame_array = cv2.cvtColor(frame_array, cv2.COLOR_BGR2GRAY)
            frame_array = frame_array.reshape(frame_array.shape + (1,))

            frames[index,:,:,:] = frame_array

    print(f'{total_records} records processed!', 99*' ')

    print("Creating model...", end="\r")

    model = create_model()

    print("Model created!", 99*' ')

    print("Training model...", end="\r")

    x_train = frames
    y_train = [angles, throttles]

    model.fit(frames, y_train, validation_split=0.1, epochs=16, verbose=1)

    print("Model trained!", 99*' ')

    print("Saving model...", end="\r")

    save_model(model)

    print("Model saved!", 99*' ')


if __name__ == "__main__":
    train_model()
