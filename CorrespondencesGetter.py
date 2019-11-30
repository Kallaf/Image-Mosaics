import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.image as mpimg
import numpy as np
import cv2
import random

def getCorrespondences(img1_url,img2_url,n):
    img=mpimg.imread(img1_url)
    imgplot = plt.imshow(img)
    print("Please select %d points" % n)
    x = plt.ginput(n)
    plt.show()

    img=mpimg.imread(img2_url)
    imgplot = plt.imshow(img)
    print("Please select %d points correspondence the points selected from image 1" % n)
    y = plt.ginput(n)
    plt.show()
    return x,y

def getCorrespondences_auto(img1_url, img2_url):

    img1 = cv2.imread(img1_url)
    img2 = cv2.imread(img2_url)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # fast = cv2.FastFeatureDetector_create()
    # surf = cv2.xfeatures2d.SURF_create(400)
    # orb = cv2.ORB_create(400)
    sift = cv2.xfeatures2d.SIFT_create(400)

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)
    # kp1, des1 = surf.detectAndCompute(gray1, None)
    # kp2, des2 = surf.detectAndCompute(gray2, None)

    # kp1 = orb.detect(gray1, None)
    # kp2 = orb.detect(gray2, None)
    # kp1, des1 = orb.compute(gray1, kp1)
    # kp2, des2 = orb.compute(gray1, kp2)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Initialize lists
    list_kp1 = []
    list_kp2 = []
    good_matches = []

    for mat in matches:
        # Apply ratio test
        if mat[0].distance < 0.7 * mat[1].distance:
            # Append good matches
            good_matches.append([mat[0]])
            # Get the matching keypoints for each of the images
            img1_idx = mat[0].queryIdx
            img2_idx = mat[0].trainIdx

            # Get the coordinates
            (x1, y1) = kp1[img1_idx].pt
            (x2, y2) = kp2[img2_idx].pt

            # Append to each list
            list_kp1.append((x1, y1))
            list_kp2.append((x2, y2))

    # # cv2.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatchesKnn(gray1, kp1, gray2, kp2, good_matches, flags=2, outImg=None)
    plt.imshow(img3), plt.show()

    return list_kp1, list_kp2
