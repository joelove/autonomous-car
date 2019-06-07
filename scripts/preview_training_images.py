from argparse import ArgumentParser

import os
import sys
import glob
import time
import json
import numpy as np
import cv2


SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
ROOT_DIR = os.path.join(SCRIPT_DIR, os.pardir)

sys.path.append(ROOT_DIR)

import config

DATA_DIR = os.path.join(ROOT_DIR, config.DATA_PATH)


def modify_brightness(image, value):
    image = image.astype('float32')
    image += value
    image = np.clip(image, 0, 255)
    image = image.astype('uint8')

    return image


def process_training_image(filepath, difference, variations):
    with open(filepath) as record_file:
        record = json.load(record_file)

        frame_filename = record["frame_filename"]
        frame_filename = frame_filename[:-4] + "_reprocessed.jpg"

        frame = cv2.imread(f'{DATA_DIR}/{frame_filename}')
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        if not variations % 2:
            variations -= 1

        variation_range = variations * difference
        range_shift = int(difference / 2)
        integer_range = int(variation_range / 2)
        range_min = -(integer_range - range_shift)
        range_max = integer_range + range_shift

        preview_images = []

        for value in range(range_min, range_max, difference):
            new_image = modify_brightness(frame, value)
            preview_images.append(new_image)

        return preview_images


def preview_training_images(difference, variations):
    print(">> Previewing training images <<")

    print("Number of image variations:", variations)
    print("Variation brightness difference:", difference)

    record_files = glob.glob(f'{DATA_DIR}/*.json')[0:100]
    total_images = len(record_files)

    for _, filepath in enumerate(record_files):
        image_variations = process_training_image(filepath, difference, variations)
        preview_image = np.concatenate(image_variations, axis=1)

        cv2.imshow('preview', preview_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1)


if __name__ == "__main__":
    parser = ArgumentParser(description='Preview the image pre-processing step')

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

    args = parser.parse_args()

    preview_training_images(args.brightness_difference, args.image_variations)
