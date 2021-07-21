import argparse
import os

import cv2 as cv2

image_directory = ""
crop_directory = "crops"
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
    global image_directory, images

    image_directory = get_directory()
    images = queue_images(image_directory)
    crop_images(images)


def get_directory():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory of images to crop")
    args = parser.parse_args()
    assert args.directory, "We need a directory with images!"
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


def crop_images(images):
    global image_directory

    cv2.namedWindow("Crop")
    cv2.setMouseCallback("Crop", crop_mouse_click)
    for f in images:
        if not os.path.isfile(os.path.join(image_directory, crop_directory, f)):
            crop_image(f)


def crop_image(f):
    global key, top_left, bot_right
    top_left = None
    bot_right = None

    while True:
        img_path = os.path.join(image_directory, f)
        img = cv2.imread(img_path)
        if top_left and bot_right:
            cv2.rectangle(img, top_left, bot_right, (255, 0, 0), 1)
        cv2.imshow("Crop", img)

        key = cv2.waitKey(10)
        if key == ord('q'):
            break

    img = cv2.imread(img_path)
    crop = img[:,:,:]
    if top_left is not None and bot_right is not None:
        crop = img[top_left[1]:bot_right[1], top_left[0]:bot_right[0],:]
    new_img_path = os.path.join(image_directory, crop_directory, f)
    print("Saving cropped image {0}".format(new_img_path))
    cv2.imwrite(new_img_path, crop)


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

