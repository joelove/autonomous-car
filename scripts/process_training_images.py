import os
import sys
import glob
import json
import numpy as np
import cv2

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
root_dir = os.path.join(script_dir, os.pardir)

sys.path.append(root_dir)

import config


def modify_brightness(image, value):
    image = image.astype('float32')
    image += value
    image = np.clip(image, 0, 255)
    image = image.astype('uint8')

    return image


def append_suffix_to_path(filepath, suffix):
    path, ext = os.path.splitext(filepath)
    return path + suffix + ext


def process_training_images():
    data_dir = os.path.join(root_dir, config.DATA_PATH)
    record_files = glob.glob(f'{data_dir}/*.json')
    total_images = len(record_files)

    frames = []
    angles = []
    throttles = []

    for index, filepath in enumerate(record_files):
        completion_ratio = float(index) / total_images
        percent_complete = int(round(completion_ratio * 100))

        print(f'Processing image {index} of {total_images}... ({percent_complete}%)', end="\r")

        with open(filepath) as record_file:
            record = json.load(record_file)

            frame_filename = record["frame_filename"]
            frame = cv2.imread(f'{data_dir}/{frame_filename}')

            for n in range(1, 5):
                new_frame = modify_brightness(frame, n * 16)
                new_record_filepath = append_suffix_to_path(filepath, f'_l{n}')
                new_image_filename = append_suffix_to_path(frame_filename, f'_l{n}')
                with open(new_record_filepath, "w") as outfile:
                    json.dump(record, outfile)
                    cv2.imwrite(f'{data_dir}/{new_image_filename}', new_frame)

            for n in range(1, 5):
                new_frame = modify_brightness(frame, -(n * 16))
                new_record_filepath = append_suffix_to_path(filepath, f'_d{n}')
                new_image_filename = append_suffix_to_path(frame_filename, f'_d{n}')
                with open(new_record_filepath, "w") as outfile:
                    json.dump(record, outfile)
                    cv2.imwrite(f'{data_dir}/{new_image_filename}', new_frame)

    print(f'{total_images} images processed!', 99*' ')


if __name__ == "__main__":
    process_training_images()
