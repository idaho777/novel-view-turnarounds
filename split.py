import argparse
import os

import cv2 as cv2
import numpy as np
from scipy.signal import find_peaks

image_directory = None
CROPS = "crops"
SPLITS = "splits"
PAD = 4
image_files = []
key = None


def split():
    global image_directory, image_files

    get_directory()
    queue_images()
    split_images()


def get_directory():
    global image_directory, CROPS
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory of images to crop")
    args = parser.parse_args()
    assert args.directory, "We need a directory with images!"
    image_directory = args.directory
    os.path.isdir(os.path.join(image_directory, CROPS))

    print("Directory {0}".format(args.directory))


def queue_images():
    global image_files, image_directory, CROPS

    for f in os.listdir(os.path.join(image_directory, CROPS)):
        img = cv2.imread(os.path.join(image_directory, CROPS, f))
        if img is not None:
            image_files.append(f)
    return image_files


def split_images():
    global image_files
    for f in image_files:
        print("Splitting {0}".format(f))
        img = cv2.imread(os.path.join(image_directory, CROPS, f))
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        entropy = calculate_entropy(img)
        splits = split_image(img, entropy)
        save_images(splits, f)


def calculate_entropy(img):
    entropy = np.apply_along_axis(calculate_col_entropy, axis=0, arr=img)
    return entropy


def calculate_col_entropy(col):
    values, counts = np.unique(col, return_counts=True)
    norm_counts = counts / counts.sum()
    base = 2
    return -(norm_counts * np.log(norm_counts)/np.log(base)).sum()


def split_image(img, entropy):
    entropy = entropy**2
    entropy = 100*entropy/np.max(entropy)
    conv_entropy = np.convolve(entropy, np.full(2*PAD+1, 1/(2*PAD+1)),mode='same')
    conv_entropy = -np.pad(conv_entropy, (PAD, PAD), mode='linear_ramp', end_values=(5,5))
    peaks, _ = find_peaks(conv_entropy, distance= int(0.70*conv_entropy.size/5), threshold=-15)
    peaks = peaks - 4
    print(peaks)

    splits = []
    for (le, ri) in zip(peaks[:-1], peaks[1:]):
        split_img = img[:, le:ri+1]
        r,w = split_img.shape

        if r % 2 == 1:
            split_img = np.pad(split_img, ((1,0),(0,0)), constant_values=255)
        if w % 2 == 1:
            split_img = np.pad(split_img, ((0,0),(1,0)), constant_values=255)

        r,w = split_img.shape
        p = int((r - w)/2)
        split_img = np.pad(split_img, ((0,0),(p, p)), constant_values=255)

        splits.append(split_img)
    
    return splits


def save_images(images, f):
    save_directory = os.path.join(image_directory, SPLITS)
    name, ext = os.path.splitext(f)
    for i in range(len(images)):
        save_name = os.path.join(save_directory, "{0}_{1}{2}".format(name, i, ext))
        cv2.imwrite(save_name, images[i])


if __name__ == '__main__':
    split()
