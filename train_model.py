
import glob
import cv2
import numpy as np

from funcy import rcompose as pipe
from keras.models import Model
from keras.layers import Input, Cropping3D, Convolution3D, MaxPooling3D, BatchNormalization, Dropout, Flatten, Dense


def save_model(model):
    with open("model.json", "w") as json_file:
        json_file.write(model.to_json())

    model.save_weights("model.h5")


def create_model():
    layers = pipe(
        Cropping3D(cropping=((0, 0), (60, 0), (0, 0))),
        Convolution3D(8, (3, 3, 3), strides=(1, 2, 2), activation='relu'),
        MaxPooling3D(pool_size=(1, 2, 2)),
        BatchNormalization(),
        Dropout(0.1),
        Flatten(name='flattened'),
        Dense(50, activation='relu'),
        Dropout(0.2),
    )

    angle_layer = Dense(15, activation='softmax', name='angle_output')
    throttle_layer = Dense(1, activation='relu', name='throttle_output')

    image_input = Input(shape=(3, 120, 160, 3))

    angle_output = pipe(layers, angle_layer)(image_input)
    throttle_output = pipe(layers, throttle_layer)(image_input)

    model = Model(inputs=[image_input], outputs=[angle_output, throttle_output])
    model.compile(optimizer='adam',
                  loss={'angle_output':'categorical_crossentropy', 'throttle_output': 'mean_absolute_error'},
                  loss_weights={'angle_output': 0.9, 'throttle_output': 0.01})

    return model


def train_model(src_directory="training_images"):
    image_directories = glob.glob(src_directory + "/*")

    X_train = []
    Y_train = []

    for _, directory in enumerate(image_directories):
        image_files = glob.glob(directory + "/*.png")

        letter = directory.split("/")[-1]
        letter_vector = np.zeros(26)
        letter_vector[ord(letter) - ord("a")] = 1

        for _, filename in enumerate(image_files):
            letter_image = cv2.imread(filename)
            letter_image = cv2.cvtColor(letter_image, cv2.COLOR_BGR2GRAY)
            letter_image = letter_image.reshape(letter_image.shape + (1,))
            X_train.append(letter_image)
            Y_train.append(letter_vector)

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    model = create_model()
    model.fit(X_train, Y_train, validation_split=0.1, epochs=5, verbose=1)

    save_model(model)


if __name__ == "__main__":
    train_model()
