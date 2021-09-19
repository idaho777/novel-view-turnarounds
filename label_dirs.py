import argparse
import json
import os
import shutil
import tkinter as tk

import numpy as np
from label_window import LabelUI

def label():
    '''
    display Window
        Load cell of 8 buttons and image in the center
        Next and back button

        Keys:   u i o
                j v l
                m , .

                keys = camera location
                k = character viewing down

                enter = next
                backspace = prev

    save json file:
        image_name : direction 0 - 7
        0 = 0 degs
        1
    '''
    args = get_argument_values()
    '''
    Load json
    Get labeled Dir
    create output dir

    '''
    with open(args.label, 'r') as f:
        label_json = json.load(f)

    # Separate Images
    label_imgs_list = [[] for i in range(8)]

    for k,v in label_json.items():
        label_imgs_list[v].append(k)

    # make_dir()
    if (os.path.isdir(args.out)):
        shutil.rmtree(args.out)
    os.makedirs(args.out)

    for i in range(8):
        curr_dir = os.path.join(args.out,f'{i}')
        os.makedirs(curr_dir)
        for file_name in label_imgs_list[i]:
            shutil.copy(os.path.join(args.directory, file_name),
                        os.path.join(curr_dir, file_name))



    # populate_dirs()



def get_argument_values():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory of labeled images")
    parser.add_argument("-o", "--out", help="Directory output of label dirs")
    parser.add_argument("-l", "--label", help="Labels file nam")
    args = parser.parse_args()
    assert args.directory, "Specify root directory of images.  This directory should have subdirectories."
    assert args.out, "Specify json location."
    assert args.label, "Specify label file."
    return args


if __name__ == '__main__':
    print('Starting Labeling...')
    label()