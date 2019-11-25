import numpy as np

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