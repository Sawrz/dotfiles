import os
import argparse
import hashlib
import cv2
import numpy as np

# ARGUMENT INTERFACE
ap = argparse.ArgumentParser()
ap.add_argument('-o', '--original', required=True, help='Path to original files.')
ap.add_argument('-c', '--copy', required=True, help='Path to copied files.')
args = ap.parse_args()

original_files = sorted(os.listdir(args.original))
copied_files = sorted(os.listdir(args.copy))

assert len(original_files) == len(copied_files)

mismatches = []
image_file_format = ['jpg', 'jpeg', 'bmp', 'png']
text_file_format = ['log', 'txt']


def get_sha256(file_name):
    with open(file_name, 'rb') as file:
        sha256_hash = hashlib.sha256(file.read())

    return sha256_hash.hexdigest()


def check_images(original_file_path, copied_file_path):
    original_image = cv2.imread(original_file_path)
    copied_image = cv2.imread(copied_file_path)

    if original_image.shape != copied_image.shape:
        return False

    return np.sum(original_image - copied_image) == 0


def check_text_files(original_file_path, copied_file_path):
    return get_sha256(file_name=original_file_path) == get_sha256(file_name=copied_file_path)


for o_file, c_file in zip(original_files, copied_files):
    assert o_file == c_file

    file_name = o_file
    file_extension = os.path.splitext(file_name)[-1]

    original_file_path = os.path.join(args.original, file_name)
    copied_file_path = os.path.join(args.copy, file_name)

    if file_extension[1:] in image_file_format:
        passed = check_images(original_file_path, copied_file_path)
    elif file_extension[1:] in text_file_format:
        passed = check_text_files(original_file_path, copied_file_path)

    if not passed:
        mismatches.append(file_name)

if len(mismatches) == 0:
    print('Your copy was successful!')
else:
    print('There are several corrupted files due to copying!')
    print('The following files are corrupted:')
    for mismatch in mismatches:
        print(mismatch)
