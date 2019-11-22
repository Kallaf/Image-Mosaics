import matplotlib.pyplot as plt
import matplotlib.image as mpimg

'Images/The White Building/image1.png'

def getCorrespondences(img1_name,img2_name,n):
    img=mpimg.imread(img1_name)
    imgplot = plt.imshow(img)
    print("Please select %d points" % n)
    x = plt.ginput(n)
    plt.show()

    img=mpimg.imread(img2_name)
    imgplot = plt.imshow(img)
    print("Please select %d points correspondence the points selected from image 1" % n)
    y = plt.ginput(n)
    plt.show()
    return x,y