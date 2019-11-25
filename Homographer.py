import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Homographer:

    def __init__(self,a,b):
        self.a = a
        self.b = b

    def setH(self):
        A = []
        B = []

        for i,a in enumerate(self.a):
            A.append(np.asarray([a[0],a[1],1,0,0,0,-a[0]*self.b[i][0],-a[1]*self.b[i][0]]))
            A.append(np.asarray([0,0,0,a[0],a[1],1,-a[0]*self.b[i][1],-a[1]*self.b[i][1]]))
            B.append(np.asarray(self.b[i][0]))
            B.append(np.asarray(self.b[i][1]))
        A = np.asarray(A)
        B = np.asarray(B)
        self.H = np.linalg.lstsq(A, B, rcond=None)[0]
        self.H = np.insert(self.H, [8], [1.0])
        self.H = self.H.reshape(3,3)

    def transform(self,p1):
        p1 = np.array(p1)
        p1 = np.insert(p1,2,1,axis = 1)
        p1 = p1.transpose()
        tempMatrix = self.H.dot(p1)
        p1_ = []
        tempMatrix = tempMatrix.transpose()
        for row in tempMatrix:
            p1_.append([row[0]/row[2],row[1]/row[2]])
        return p1_

    def testH(self,img2_url):
        img=mpimg.imread(img2_url)
        imgplot = plt.imshow(img)
        p1_ = self.transform(self.a)
        for p in p1_:
            plt.scatter(p[0],p[1], s=30)
        plt.show()