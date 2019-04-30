import sys
import cv2
import glob
import json
import numpy as np
import re
import config

from funcy import rcompose as pipe
from keras.models import Model
from keras.layers import Input, Cropping3D, Convolution2D, MaxPooling3D, BatchNormalization, Dropout, Flatten, Dense


def save_model(model):
    with open("model.json", "w") as json_file:
        json_file.write(model.to_json())

    model.save_weights("model.h5")


def create_model():
    image_input = Input(shape=(120, 160, 1))

    hidden_layers = pipe(
        Convolution2D(filters=24, kernel_size=(5, 5), strides=(2, 2), activation='relu'),
        BatchNormalization(),
        Dropout(0.1),
        Flatten(name='flattened'),
        Dense(50, activation='relu'),
        Dropout(0.2),
    )

    angle_output_layer = pipe(
        Dense(1, activation='sigmoid'),
        Dense(1, activation='linear', name='angle_output')
    )

    throttle_output_layer = Dense(1, activation='sigmoid', name='throttle_output')

    angle_output = pipe(hidden_layers, angle_output_layer)(image_input)
    throttle_output = pipe(hidden_layers, throttle_output_layer)(image_input)

    model = Model(inputs=[image_input], outputs=[angle_output, throttle_output])
    model.compile(optimizer='adam',
                  loss={'angle_output':'mean_absolute_error', 'throttle_output': 'mean_absolute_error'},
                  loss_weights={'angle_output': 0.9, 'throttle_output': 0.01})

    return model


def train_model():
    record_files = glob.glob(f'{config.DATA_PATH}/*.json')
    total_records = len(record_files)

    frames = []
    angles = []
    throttles = []

    for index, filepath in enumerate(record_files):
        completion_ratio = float(index) / total_records
        percent_complete = int(round(completion_ratio * 100))

        print(f'Processing record {index} of {total_records}... ({percent_complete}%)', end="\r")

        with open(filepath) as record_file:
            record = json.load(record_file)

            angle = record["angle"]
            throttle = record["throttle"]

            angles.append(angle)
            throttles.append(throttle)

            frame_filename = record["frame_filename"]

            frame_array = cv2.imread(f'{config.DATA_PATH}/{frame_filename}')
            frame_array = cv2.cvtColor(frame_array, cv2.COLOR_BGR2GRAY)
            frame_array = frame_array.reshape(frame_array.shape + (1,))
            frame_array = frame_array / 255.0

            frames.append(frame_array)

    print(f'{total_records} records processed!', 99*' ')

    print("Creating model...", end="\r")

    model = create_model()

    print("Model created!", 99*' ')

    print("Training model...", end="\r")

    X_train = np.array(frames)
    Y_train = [np.array(angles), np.array(throttles)]

    model.fit(X_train, Y_train, validation_split=0.2, epochs=5, verbose=1)

    print("Model trained!", 99*' ')

    print("Saving model...", end="\r")

    save_model(model)

    print("Model saved!", 99*' ')


if __name__ == "__main__":
    train_model()
