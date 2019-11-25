import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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