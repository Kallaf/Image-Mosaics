from CorrespondencesGetter import getCorrespondences
from Homographer import Homographer
from Warpper import Warpper
import cv2
import numpy as np

folderUrl = 'Images/The White Building/'
img1_url = folderUrl + 'image1.png'
img2_url = folderUrl + 'image2.png'

n = 54

try:
    a,b = getCorrespondences(img1_url, img2_url)
    # a = [(210.52419354838707, 200.89758064516127), (210.52419354838707, 206.28870967741932), (234.39919354838707, 199.3572580645161), (235.16935483870964, 206.28870967741932), (282.91935483870964, 183.1838709677419), (282.91935483870964, 198.58709677419353), (282.91935483870964, 210.13951612903224), (214.375, 236.32499999999996), (285.2298387096774, 235.55483870967737),(272.9072580645161, 100.77661290322578), (283.68951612903226, 125.42177419354837), (300.633064516129, 118.49032258064514), (319.116935483871, 123.11129032258063), (329.1290322580645, 119.26048387096773), (340.68145161290323, 119.26048387096773), (354.54435483870964, 125.42177419354837), (362.2459677419355, 122.34112903225804), (374.56854838709677, 122.34112903225804),(353.0040322580645, 138.51451612903224), (361.47580645161287, 138.51451612903224), (353.0040322580645, 143.9056451612903), (362.2459677419355, 146.21612903225804), (356.0846774193548, 156.99838709677417), (359.93548387096774, 156.99838709677417), (373.0282258064516, 157.76854838709676), (378.41935483870964, 157.76854838709676),(369.17741935483866, 138.51451612903224), (379.18951612903226, 138.51451612903224), (370.71774193548384, 145.44596774193548), (379.18951612903226, 146.21612903225804), (286.77016129032256, 240.17580645161286), (293.7016129032258, 240.17580645161286), (299.09274193548384, 240.17580645161286), (304.4838709677419, 240.94596774193545)]
    # b = [(36.94153225806451, 186.55927419354836), (36.177419354838705, 192.67217741935482), (61.39314516129032, 187.32338709677418), (61.39314516129032, 194.20040322580644), (112.58870967741933, 170.51290322580644), (112.58870967741933, 185.03104838709675), (112.58870967741933, 199.54919354838708), (37.70564516129032, 223.23669354838705), (111.06048387096774, 223.23669354838705),(108.7681451612903, 87.98870967741937), (119.46572580645159, 113.20443548387095), (133.21975806451613, 107.85564516129031), (152.32258064516128, 113.20443548387095), (161.49193548387095, 112.44032258064516), (173.71774193548384, 112.44032258064516), (184.41532258064515, 119.31733870967741), (193.58467741935482, 116.26088709677418), (203.5181451612903, 118.55322580645162),(183.65120967741933, 130.77903225806452), (190.5282258064516, 130.77903225806452), (183.65120967741933, 135.36370967741934), (188.99999999999997, 137.65604838709677), (184.41532258064515, 147.58951612903223), (188.99999999999997, 147.58951612903223), (199.69758064516128, 148.35362903225806), (205.0463709677419, 149.11774193548385),(198.9334677419355, 133.07137096774193), (205.0463709677419, 133.83548387096772), (198.16935483870964, 138.42016129032257), (205.0463709677419, 138.42016129032257), (114.88104838709677, 228.58548387096772), (120.22983870967741, 228.58548387096772), (124.81451612903226, 228.58548387096772), (130.1633064516129, 228.58548387096772)]

    # print(b)
    # print("len", len(a), len(b))

    assert len(a) == len(b)

    homographer = Homographer(a, b)
    homographer.setH()
    homographer.testH(img2_url)
    homographer.testH_inverse(img1_url)

    warpper = Warpper(img1_url, img2_url, homographer)
    warpper.warp()
    warpper.merge_images()

except Exception as e:
    print(e)
    exit(0)


#
#  our homography matrix
# [[-2.70071693e-01 -5.42288720e-01  1.85006968e+02]
#  [-2.68285965e-01 -4.95622550e-01  1.74499361e+02]
#  [-1.49967768e-03 -2.87100038e-03  1.00000000e+00]]
#
# cv2 homography matrix
# [[-3.63666414e-01 -5.06289033e-01  1.91331216e+02]
#  [-3.17154620e-01 -4.43908054e-01  1.67440355e+02]
#  [-1.90149423e-03 -2.64276533e-03  1.00000000e+00]]
#
# difference between the two matricies
# [[-9.35947210e-02  3.59996876e-02  6.32424809e+00]
#  [-4.88686552e-02  5.17144962e-02 -7.05900616e+00]
#  [-4.01816544e-04  2.28235051e-04  0.00000000e+00]]
#