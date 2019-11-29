from Homographer import Homographer
from PIL import Image
import numpy as np
import scipy.misc as smp

class Warpper:

    def warp(self,img1_url,img2_url,homographer):
        im = Image.open(img1_url)
        width,height = im.size
        x = np.arange(0, width, 1)
        y = np.arange(0, height, 1)
        X,Y = np.meshgrid(x, y)
        new_corr = []
        mnx = mny = mxx = mxy = 0
        for i,rowY in enumerate(X):
            row = Y[i]
            p = np.vstack((row, rowY)).T
            p_ = np.array(homographer.transform(p))
            xmax, ymax = p_.max(axis=0)
            xmin, ymin = p_.min(axis=0)

            #print(xmin,ymin,xmax,ymax)
            mnx = min(xmin,mnx)
            mny = min(ymin,mny)
            mxx = max(xmax,mxx)
            mxy = max(ymax,mxy)
            new_corr.append(p_)


        print(mnx,mny,mxx,mxy)
        im2 = Image.open(img2_url)
        width2,height2 = im2.size
        data = np.zeros( (int(max(mxy,height2)-mny+1),int(max(mxx,width2)-mnx+1),4), dtype=np.uint8 )
        pix = list(im2.getdata())
        pix = np.reshape(pix, (height2, width2,4))

        for x in range(0,width2):
            for y in range(0,height2):
                temp = pix[y][x]
                data[int(y-mny),int(x-mnx)] = temp
        pix = list(im.getdata())
        pix = np.reshape(pix, (height,width,4))
        

        for i,row in enumerate(new_corr):
            for j,corr in enumerate(row):
                    x = int(corr[0] - mnx)
                    y = int(corr[1] - mny)
                    temp = pix[i][j]
                    data[x,y] = temp
        img = smp.toimage( data )       # Create a PIL image
        img.show()