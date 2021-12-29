# coding: utf-8
"""
Created on Thu Jul 15 17:00 2021

@author: 及川弘登
"""

import cv2
import numpy as np
def re_main():
    for i in range(1):
        x = 0
        y = 0
        pic_name="redcorn"+str(i+1)+ ".jpg"
        pic_name_out="redcorn"+str(i+1)+ "out.jpg"
        gray_pic="redcorn"+str(i+1)+ "gray.jpg"
        img = cv2.imread(pic_name,cv2.IMREAD_COLOR)
        height, width = img.shape[:2]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]
        img_redcorn=np.zeros((height,width,3),np.uint8)
        img_redcorn[(h <13) & (h > 0) & (s > 96.7)& (v > 98.4)] = 255
        cv2.imwrite(gray_pic,np.array(img_redcorn))
        img_gray = cv2.imread(gray_pic,cv2.IMREAD_GRAYSCALE)
        M = cv2.moments(img_gray, False)
        contours, hierarchy= cv2.findContours(img_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x,y= int(M["m10"]/(M["m00"]+1)) , int(M["m01"]/(M["m00"]+1))
        #Zerodivision_kaihi
        cv2.circle(img, (x,y), 20, 100, 2, 4)
        cv2.drawContours(img, contours, -1, color=(0, 0, 0), thickness=5)
        cv2.imwrite(pic_name_out,np.array(img))
        out = [x , y]
        return out
if __name__ == '__main__':
    re_main()
