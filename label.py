import argparse
import json
import os
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
    main_window = create_window()
    main_window.load_directory(*get_directory())
    main_window.mainloop()


def create_window():
    main_window = LabelUI(tk.Tk())
    return main_window


def get_directory():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory of images to crop")
    parser.add_argument("-o", "--out", help="Location of json file of labels")
    args = parser.parse_args()
    assert args.directory, "Specify root directory of images.  This directory should have subdirectories."
    assert args.out, "Specify json location."
    print("Directory {0}".format(args.directory))
    return args.directory, args.out


if __name__ == '__main__':
    print('Starting Labeling...')
    label()
