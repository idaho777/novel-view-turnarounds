import argparse
import os

import cv2 as cv2

image_directory = "0-originals"
crop_directory = "1-crops"
images = []
key = None
top_left = None
bot_right = None

def split():
    '''
    Get directory of images
    Setup gui box
    For each image
       fit image to gui box
       Allow 2 clicks
       Show box to crop image
       press 'Enter'

    '''
    global image_directory, crop_directory
    main_directory = get_directory()
    image_directory = os.path.join(main_directory, image_directory)
    crop_directory = os.path.join(main_directory, crop_directory)

    if not os.path.isdir(crop_directory):
        os.mkdir(crop_directory)

    images = queue_images(os.path.join(main_directory, image_directory))
    crop_images(images)


def get_directory():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory of images to crop")
    args = parser.parse_args()
    assert args.directory, "Specify root directory of images.  This directory should have subdirectories."
    print("Directory {0}".format(args.directory))
    return args.directory


def queue_images(image_directory):
    images = []
    for f in os.listdir(image_directory):
        img_path = os.path.join(image_directory, f)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(f)
    return images


def crop_images(orig_images):
    global image_directory, crop_directory

    cv2.namedWindow("Crop")
    cv2.setMouseCallback("Crop", crop_mouse_click)
    for i in range(len(orig_images)):
        f = orig_images[i]
        if not os.path.isfile(os.path.join(crop_directory, f)): # If cropped image doesn't exist
            print("{0}/{1}: Cropping {2}".format(i, len(orig_images), f))
            crop_image(f)


def crop_image(f):
    global key, top_left, bot_right
    top_left = None
    bot_right = None

    img_path = os.path.join(image_directory, f)
    while True:
        img = cv2.imread(img_path)
        if top_left and bot_right:
            cv2.rectangle(img, top_left, bot_right, (255, 0, 0), 1)
        cv2.imshow("Crop", img)

        key = cv2.waitKey(10)
        if key == ord('q'):
            img = cv2.imread(img_path)
            crop = img[:,:,:]
            if top_left is not None and bot_right is not None:
                crop = img[top_left[1]:bot_right[1], top_left[0]:bot_right[0],:]

            new_img_path = os.path.join(crop_directory, f)
            print("Saving cropped")
            cv2.imwrite(new_img_path, crop)
            break
        if key == ord('s'):
            print("Skip image")
            break



def crop_mouse_click(event, x, y, flags, param):
    global key, top_left, bot_right
    if event == cv2.EVENT_LBUTTONUP:
        top_left = (x, y)
    elif event == cv2.EVENT_RBUTTONUP:
        bot_right = (x, y)
    else:
        return


if __name__ == '__main__':
    split()
