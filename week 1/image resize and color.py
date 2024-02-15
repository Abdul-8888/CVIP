
import cv2
import numpy as np

"""Fetching image"""
image = cv2.imread("D:/Current Courses/CVIP/week 1/image.jpg")
# print(image.shape)
# cv2.imshow("image", image)

"""Getting RGB values"""
B = image[:,:,0]
G = image[:,:,1]
R = image[:,:,2]

# cv2.imshow("blue", B)
# cv2.imshow("green", G)
# cv2.imshow("red", R)

"""Making image to only one color scale"""
Z = np.zeros((image.shape[0], image.shape[1]))

# image[:,:,1] = Z
# image[:,:,2] = Z

# cv2.imshow("blue", B)

"""changing size of the image/Copying a part of the image"""
ROI = image[0:200, 0:200, :]
# print(ROI)
cv2.imshow("roi", ROI)

"""Pasting the copied part"""
image[200:400, 200:400, :] = ROI
# image[500:1000, 100:200] = cv2.resize(ROI, (100, 500))
cv2.imshow("copied image", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
