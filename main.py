from CorrespondencesGetter import getCorrespondences
from Homographer import Homographer
import cv2
import numpy as np

folderUrl = 'Images/The White Building/'
img1_url = folderUrl + 'image1.png'
img2_url = folderUrl + 'image2.png'

a,b = getCorrespondences(img1_url,img2_url,4)


homographer = Homographer(a,b)
homographer.setH()
homographer.testH(img2_url)