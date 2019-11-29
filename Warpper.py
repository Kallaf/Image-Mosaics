from Homographer import Homographer
from PIL import Image
import numpy as np
import scipy.misc as smp


class Warpper:

    def warp(self,img1_url,homographer):
        im = Image.open(img1_url)
        width,height = im.size
        x = np.arange(0, width, 1)
        y = np.arange(0, height, 1)
        X,Y = np.meshgrid(x, y)
        new_corr = []
        self.mnx = self.mny = self.mxx = self.mxy = 0
        for i,col in enumerate(X):
            row = Y[i]
            p = np.vstack((col,row)).T
            p_ = np.array(homographer.transform(p))
            xmax, ymax = p_.max(axis=0)
            xmin, ymin = p_.min(axis=0)

            #print(xmin,ymin,xmax,ymax)
            self.mnx = min(xmin,self.mnx)
            self.mny = min(ymin,self.mny)
            self.mxx = max(xmax,self.mxx)
            self.mxy = max(ymax,self.mxy)
            new_corr.append(p_)

        print(self.mxx,self.mxy)
        self.data = np.zeros( (int(self.mxy-self.mny+2),int(self.mxx-self.mnx+2),4), dtype=np.uint8 )
        pix = list(im.getdata())
        pix = np.reshape(pix, (height,width,4))
        

        for i,row in enumerate(new_corr):
            for j,corr in enumerate(row):
                    x = int(corr[0] - self.mnx + 0.5)
                    y = int(corr[1] - self.mny + 0.5)
                    self.data[y][x] = pix[i][j]

        
        wrapped_img = smp.toimage( self.data )       # Create a PIL image
        wrapped_img.show()
        


    def merge_images(self,img_url):
        im = Image.open(img_url)
        width,height = im.size
        print(width,height)
        data = np.zeros( (int(max(height,self.mxy)-self.mny+2),int(max(width,self.mxx)-self.mnx+2),4), dtype=np.uint8 )
        
        

        for y in range(0,len(self.data)):
            for x in range(0,len(self.data[y])):
                data[y][x] = self.data[y][x]

        pix = list(im.getdata())
        pix = np.reshape(pix, (height,width,4))
        for x in range(0,width):
            for y in range(0,height):
                data[int(y-self.mny),int(x-self.mnx)] = pix[y][x] 


        final_img = smp.toimage( data )       # Create a PIL image
        final_img.show()        