
"""Assignment: create a utility to make a collage of any number of images."""

import cv2
import numpy as np
import glob

path = 'D:/Current Courses/CVIP/week 1/*'
extension = 'jpg'

files = glob.glob(f'{path}.{extension}')

min_height = float('inf')
min_width = float('inf')

for f in files:
    img = cv2.imread(f)
    if img is not None:
        h, w = img.shape[:2]
        min_height = min(h, min_height)
        min_width = min(w, min_width)

images = []
collage_width = 0
for f in files:
    img = cv2.imread(f)
    if img is not None:
        resized_img = cv2.resize(img, (min_width, min_height))
        images.append(resized_img)
        collage_width += min_width

collage = np.zeros((min_height, collage_width, 3), dtype=np.uint8)

current_width = 0
for img in images:
    collage[:, current_width:current_width + min_width] = img
    current_width += min_width

cv2.imshow("Collage", collage)
cv2.waitKey(0)
cv2.destroyAllWindows()
