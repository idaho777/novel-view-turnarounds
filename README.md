# novel-view-turnarounds
This is a small script to prepare turnaround poses from character turnaround/reference sheets.  Lots of things are hard-coded.

First we crop the turnaround into a smaller image with 5 poses side-by-side.  Then we split the image into 5 individual pose images.

`crop.py` is an interactive script.  Users can draw a rectangle using left-mouse for the top-left corner and right-mouse for the bottom-right corner.  Pressing `q` will then crop the image and save it (or not crop if there you think the image is fine).

`split.py` then splits the 5 poses x 1 pose image into 5 individual pose images.  We split the images by low vertical entropy.
