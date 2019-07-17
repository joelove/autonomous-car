from PIL import Image

import os
import glob
import sys
import cv2

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
root_dir = os.path.join(script_dir, os.pardir)

sys.path.append(root_dir)

from utilities.image_filters import apply_default_filters

import config


data_dir = os.path.join(root_dir, config.DATA_PATH)
raw_image_files = glob.glob(f'{data_dir}/*_raw.jpg')

for filepath in raw_image_files:
    print(filepath)
    raw_image_file = cv2.imread(filepath)

    filtered_image = apply_default_filters(raw_image_file)
    filtered_image_array = Image.fromarray(filtered_image)

    new_path = filepath[:-4] + "_reprocessed.jpg"

    filtered_image_array.save(new_path)
