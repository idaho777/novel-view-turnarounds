import argparse
import os
import shutil

import cv2 as cv2
import numpy as np
from scipy.signal import find_peaks

import peakdetect as peakdetect

crop_directory = "1-crops"
split_directory = "2-splits"
PAD = 2
image_files = []
key = None


def split():
    global image_directory, image_files

    get_directory()
    queue_images()
    split_images()


def get_directory():
    global crop_directory, split_directory
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory of images to crop")
    args = parser.parse_args()
    assert args.directory, "We need a directory with images!"
    root_directory = args.directory
    crop_directory = os.path.join(root_directory, crop_directory)
    split_directory = os.path.join(root_directory, split_directory)


def queue_images():
    global image_files, image_directory, crop_directory

    for f in os.listdir(crop_directory):
        img = cv2.imread(os.path.join(crop_directory, f))
        if img is not None:
            image_files.append(f)
    return image_files


def split_images():
    global image_files

    if os.path.isdir(split_directory):
        shutil.rmtree(split_directory)
    os.mkdir(split_directory)

    for f in image_files:
        print("Splitting {0}".format(f))
        img = cv2.imread(os.path.join(crop_directory, f))
        img_bw = np.copy(img)
        if len(img_bw.shape) > 2:
            img_bw = cv2.cvtColor(img_bw, cv2.COLOR_BGR2GRAY)

        entropy = calculate_entropy(img_bw)
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
    # entropy = 100*entropy/np.max(entropy)
    entropy = np.convolve(entropy, np.full(2*PAD+1, 1/(2*PAD+1)), mode='same')
    max_entropy = max(entropy)
    min_entropy = min(entropy)
    entropy = np.pad(entropy, (PAD, PAD), mode='linear_ramp', end_values=(max_entropy, max_entropy))
    # # peaks, _ = find_peaks(conv_entropy, distance= int(0.70*conv_entropy.size/5), threshold=-15)
    # peaks, v = find_peaks(conv_entropy, threshold=-15)
    # peaks = peaks - 4
    # print(peaks)
    # print(v)

    maxtab, mintab = peakdetect.peakdet(entropy, (max_entropy-min_entropy)*0.5)
    #mintab = [x for x in mintab if x[1] < ((max_entropy + min_entropy)/2)*0.9]

    # from matplotlib.pyplot import plot, scatter, show
    # plot(entropy)
    # scatter(np.array(mintab)[:,0], np.array(mintab)[:,1], color='blue')
    # scatter(np.array(maxtab)[:,0], np.array(maxtab)[:,1], color='red')
    # show()

    if len(img.shape) < 3:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    peaks = [int(x[0]) for x in mintab]
    splits = []
    for (le, ri) in zip(peaks[:-1], peaks[1:]):
        split_img = img[:, le:ri+1, :]
        r,w,_ = split_img.shape

        if r % 2 == 1:
            split_img = np.pad(split_img, ((1,0),(0,0),(0,0)), constant_values=255)
        if w % 2 == 1:
            split_img = np.pad(split_img, ((0,0),(1,0),(0,0)), constant_values=255)

        r,w,_ = split_img.shape
        p = int(abs(r - w)/2)
        split_img = np.pad(split_img, ((0,0),(p, p),(0,0)), constant_values=255)

        splits.append(split_img)
    return splits


def save_images(images, f):
    name, ext = os.path.splitext(f)
    for i in range(len(images)):
        save_name = os.path.join(split_directory, "{0}_{1}{2}".format(name, i, ext))
        cv2.imwrite(save_name, images[i])


if __name__ == '__main__':
    split()
