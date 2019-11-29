from Homographer import Homographer
from PIL import Image
import numpy as np
import scipy.misc as smp
from scipy.interpolate import RectBivariateSpline

class Warpper:

    def __init__(self,img1_url,img2_url,homographer):
        self.im1 = Image.open(img1_url)
        self.im2 = Image.open(img2_url)
        self.homographer = homographer
    
    def interpolate(self,channel_no):
        channel = self.pix[:,:,channel_no]
        interp_spline = RectBivariateSpline(self.img1_y,self.img1_x, channel)
        return interp_spline(self.warpped_y,self.warpped_x)

    def inverse_warp(self):
        x = np.arange(self.mnx, self.mxx, 1)
        y = np.arange(self.mny, self.mxy, 1)
        X,Y = np.meshgrid(x,y)
        new_corr = []
        mnx = mny = mxx = mxy = 0
        for i,col in enumerate(X):
            row = Y[i]
            p_ = np.vstack((col,row)).T
            p = np.array(self.homographer.inverse_transform(p_))
            xmax, ymax = p.max(axis=0)
            xmin, ymin = p.min(axis=0)

            #print(xmin,ymin,xmax,ymax)
            mnx = min(xmin,mnx)
            mny = min(ymin,mny)
            mxx = max(xmax,mxx)
            mxy = max(ymax,mxy)
            new_corr.append(p)
        height = mxy-mny
        width = mxx-mnx
        self.warpped_x = np.arange(0, width, 1)
        self.warpped_y = np.arange(0, height, 1)
        
        channels = []
        for channel_no in range(4):
            channels.append(self.interpolate(channel_no))

        for i,row in enumerate(new_corr):
            for j,corr in enumerate(row):
                    x = int(corr[0])
                    y = int(corr[1])
                    if x >= 0 and y >=0:
                        self.data[i][j] = [channels[0][y][x],channels[1][y][x],channels[2][y][x],channels[3][y][x]]


    def warp(self):
        width,height = self.im1.size
        self.img1_x = np.arange(0, width, 1)
        self.img1_y = np.arange(0, height, 1)
        X,Y = np.meshgrid(self.img1_x, self.img1_y)
        new_corr = []
        self.mnx = self.mny = self.mxx = self.mxy = 0
        for i,col in enumerate(X):
            row = Y[i]
            p = np.vstack((col,row)).T
            p_ = np.array(self.homographer.transform(p))
            xmax, ymax = p_.max(axis=0)
            xmin, ymin = p_.min(axis=0)

            #print(xmin,ymin,xmax,ymax)
            self.mnx = min(xmin,self.mnx)
            self.mny = min(ymin,self.mny)
            self.mxx = max(xmax,self.mxx)
            self.mxy = max(ymax,self.mxy)
            new_corr.append(p_)

        self.warpped_height = int(self.mxy-self.mny+2)
        self.warpped_width = int(self.mxx-self.mnx+2)
        self.data = np.zeros( (self.warpped_height,self.warpped_width,4), dtype=np.uint8 )
        self.pix = list(self.im1.getdata())
        self.pix = np.reshape(self.pix, (height,width,4))
        

        for i,row in enumerate(new_corr):
            for j,corr in enumerate(row):
                    x = int(corr[0] - self.mnx + 0.5)
                    y = int(corr[1] - self.mny + 0.5)
                    self.data[y][x] = self.pix[i][j]

        
        wrapped_img = Image.fromarray( self.data )       # Create a PIL image
        wrapped_img.show()
        self.inverse_warp()
        wrapped_img = Image.fromarray( self.data )       # Create a PIL image
        wrapped_img.show()
        


    def merge_images(self):
        width,height = self.im2.size
        data = np.zeros( (int(max(height,self.mxy)-self.mny+2),int(max(width,self.mxx)-self.mnx+2),4), dtype=np.uint8 )
        
        
        for y in range(0,self.warpped_height):
            for x in range(0,self.warpped_width):
                if self.data[y][x].any() != 0:
                    data[y][x] = self.data[y][x]

        pix = list(self.im2.getdata())
        pix = np.reshape(pix, (height,width,4))
        for x in range(0,width):
            for y in range(0,height):
                data[int(y-self.mny),int(x-self.mnx)] = pix[y][x] 


        final_img = Image.fromarray( data )       # Create a PIL image
        final_img.show()