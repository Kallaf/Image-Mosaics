import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

class Homographer:

    def __init__(self,a,b):
        self.a = a
        self.b = b
        # print("a = ",a)
        # print("b = ",b)

    def setH(self):
        A = []
        B = []

        for i,a in enumerate(self.a):
            b = self.b[i]
            A.append(np.asarray([a[0],a[1],1,0,0,0,-a[0]*b[0],-a[1]*b[0]]))
            A.append(np.asarray([0,0,0,a[0],a[1],1,-a[0]*b[1],-a[1]*b[1]]))
            B.append(np.asarray(b[0]))
            B.append(np.asarray(b[1]))
        A = np.asarray(A)
        B = np.asarray(B)
        self.H = np.linalg.lstsq(A, B, rcond=None)[0]
        self.H = np.insert(self.H, [8], [1.0])
        self.H = self.H.reshape(3,3)
        print("our homography matrix")
        print(self.H)
        print()
        H, status = cv2.findHomography(np.asarray(self.a),np.asarray(self.b), cv2.RANSAC, 5.0)

        print("cv2 homography matrix")
        print(H)
        print()

        print("difference between the two matricies")
        print(np.subtract(H,self.H))
        print("total error = ",sum(sum(abs(np.subtract(H,self.H))))//9)
        print()
        print()
        self.H = H
        
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

    def inverse_transform(self,p1_):
        p1_ = np.array(p1_)
        p1_ = np.insert(p1_,2,1,axis = 1)
        p1_ = p1_.transpose()
        tempMatrix = np.linalg.inv(self.H).dot(p1_)
        p1 = []
        tempMatrix = tempMatrix.transpose()
        for row in tempMatrix:
            p1.append([row[0]/row[2],row[1]/row[2]])
        return p1

    def testH(self,img2_url):
        img=mpimg.imread(img2_url)
        plt.imshow(img)
        p1_ = self.transform(self.a)

        for p in p1_:
            plt.scatter(p[0],p[1], s=30)
        plt.show()

    def testH_inverse(self,img1_url):
        img=mpimg.imread(img1_url)
        plt.imshow(img)
        p1_ = self.inverse_transform(self.b)
        for p in p1_:
            plt.scatter(p[0],p[1], s=30)
        plt.show()
