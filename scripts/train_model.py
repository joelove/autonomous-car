import os
import sys
import cv2
import glob
import json
import numpy as np
import random
import datetime

from preview_training_images import process_training_image

from argparse import ArgumentParser

from tensorflow.keras.models import Model, model_from_json
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Input, Convolution2D, BatchNormalization, Dropout, Flatten, Dense
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras import backend as TfBackend

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
root_dir = os.path.join(script_dir, os.pardir)

sys.path.append(root_dir)

import config


def save_model(model, name):
    with open(f'{name}.json', "w") as json_file:
        json_file.write(model.to_json())

    model.save_weights(f'{name}.h5')


def create_model(args):
    image_shape = tuple(reversed(config.CAMERA_FINAL_RESOLUTION))
    image_input = Input(shape=((116, 205), 1))

    x = image_input

    channels = 8
    while (channels <= args.max_channels):
        x = BatchNormalization()(x)
        x = Convolution2D(channels, (3, 3), strides=(2, 2), activation='relu')(x)

        if args.dropouts:
            x = Dropout(0.2)(x)

        channels *= 2

    x = BatchNormalization()(x)
    x = Convolution2D(args.max_channels, (3, 3), strides=(2, 2), activation='relu')(x)

    x = Flatten(name='flattened')(x)
    x = BatchNormalization()(x)
    x = Dense(args.dense_size, activation='relu')(x)

    angle_output = Dense(1, activation='tanh', name='angle_output')(x)
    throttle_output = Dense(1, activation='sigmoid', name='throttle_output')(x)

    model = Model(inputs=[image_input], outputs=[angle_output, throttle_output])
    model.compile(optimizer=Adam(lr=3e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-5, decay=0.0, amsgrad=False),
                  loss={'angle_output':'mean_absolute_error', 'throttle_output': 'mean_absolute_error'},
                  loss_weights={'angle_output': 0.9, 'throttle_output': 0.01})

    return model


def train_model(args):
    print(">> Training model <<")

    print("Dense layer size:", args.dense_size)
    print("Include dropout layers:", "Yes" if args.dropouts else "No")
    print("Maximum convolutional layer channels:", args.max_channels)
    print("Total epochs:", args.epochs)
    print("Validation data split:", args.validation_split)
    print("Total training epochs:", args.epochs)
    print("Number of image variations:", args.image_variations)
    print("Variation brightness difference:", args.brightness_difference)
    print("Learning rate (alpha):", args.learning_rate)

    if args.model:
        print("Existing model:", args.model + ".*")

    data_dir = os.path.join(root_dir, config.DATA_PATH)
    record_files = glob.glob(f'{data_dir}/*.json')

    total_records = len(record_files)
    image_shape = tuple(reversed(config.CAMERA_FINAL_RESOLUTION))

    image_variations = args.image_variations

    if not image_variations % 2:
        image_variations -= 1

    total_variations = total_records * image_variations

    frames = np.empty((total_variations, *image_shape, 1))
    angles = np.empty(total_variations)
    throttles = np.empty(total_variations)

    index = 0

    for filepath in record_files:
        completion_ratio = float(index) / total_variations
        percent_complete = int(round(completion_ratio * 100))

        print(f'Processing record {index + 1} of {total_variations}... ({percent_complete}%)', end="\r")

        with open(filepath) as record_file:
            record = json.load(record_file)

            angle = record["angle"]
            throttle = record["throttle"]

            frame_variations = process_training_image(filepath, args.brightness_difference, image_variations)

            for frame_variation in frame_variations:
                frame_array = frame_variation.reshape((116, 205) + (1,))

                angles[index] = angle
                throttles[index] = throttle
                frames[index,:,:,:] = frame_array

                index += 1

    print(f'{total_records} records processed!', 99*' ')

    if args.model:
        print(f'Loading model from {args.model}.*...')
        json_file = open(f'{args.model}.json', "r")
        loaded_model_json = json_file.read()

        json_file.close()

        model = model_from_json(loaded_model_json)
        model.load_weights(f'{args.model}.h5')
        model.compile(optimizer=Adam(lr=args.learning_rate, beta_1=0.9, beta_2=0.999, epsilon=1e-5, decay=0.0, amsgrad=False),
                      loss={'angle_output':'mean_absolute_error', 'throttle_output': 'mean_absolute_error'},
                      loss_weights={'angle_output': 0.9, 'throttle_output': 0.01})
    else:
        print("Creating model...", end="\r")
        model = create_model(args)
        print("Model created!", 99*' ')

    print("Training model...", end="\r")

    x_train = frames
    y_train = [angles, throttles]

    date = datetime.datetime.now().strftime('%y-%m-%d-%H-%M')
    tb_callback = TensorBoard(log_dir=('./tensorboard_logs/%s' % date), histogram_freq=0, write_graph=True, write_images=True)

    model.fit(x_train, y_train, validation_split=args.validation_split, epochs=args.epochs, verbose=1, callbacks=[tb_callback])

    print("Model trained!", 99*' ')
    print("Saving model...", end="\r")

    save_model(model, f'{datetime.datetime.now().strftime("%y-%m-%d-%H-%M")}_model')

    print("Model saved!", 99*' ')


if __name__ == "__main__":
    parser = ArgumentParser(description='Train the model using captured data')

    parser.add_argument("-d", "--dropouts",
                        help="enable dropout layers",
                        action="store_true",
                        dest="dropouts",
                        default=False)

    parser.add_argument("-s", "--size",
                        help="set size of final dense layer [default: 128]",
                        action="store",
                        dest="dense_size",
                        type=int,
                        default=128)

    parser.add_argument("-m", "--max-channels",
                        help="set maximum channels for convolution layers [default: 64]",
                        action="store",
                        dest="max_channels",
                        type=int,
                        default=64)

    parser.add_argument("-e", "--epochs",
                        help="set number of training epochs [default: 8]",
                        action="store",
                        dest="epochs",
                        type=int,
                        default=8)

    parser.add_argument("-v", "--validation-split",
                        help="set the amount of data that should be used for validation [default: 0.1]",
                        action="store",
                        dest="validation_split",
                        type=float,
                        default=0.1)

    parser.add_argument("-i", "--image-variations",
                        help="specify the number of image variations to be generated [default: 3]",
                        dest="image_variations",
                        action="store",
                        type=int,
                        default=3)

    parser.add_argument("-b", "--brightness-difference",
                        help="specify the brightness difference between variations [default: 32]",
                        dest="brightness_difference",
                        action="store",
                        type=int,
                        default=32)

    parser.add_argument("-l", "--load-model",
                        help="specify an existing model to start from",
                        dest="model",
                        action="store",
                        default=False)

    parser.add_argument("-a", "--learning-rate",
                        help="specify the learning rate (alpha) [default: 3e-4]",
                        dest="learning_rate",
                        action="store",
                        type=float,
                        default=3e-4)

    args = parser.parse_args()

    train_model(args)

    TfBackend.clear_session()
