#!/usr/bin/python
#coding: UTF-8

import cv2
import cv2.cv as cv

class USBCamera:

    """デフォルト・コンストラクター。"""
    def __init__(self, width=640, height=480):
        self.capture = cv2.VideoCapture(-1)
        if self.capture.isOpened() is False:
            rise("IO Error")
        self.capture.set(cv.CV_CAP_PROP_FRAME_WIDTH,width)
        self.capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT,height)
        
        # 取得一回目は、ごみデーターが入るため、ここで読み飛ばす。
        self.capture.read()
    
    """デストラクター。"""
    def __del__(self):
        del(self.capture)

    """画像ファイルの取得。"""
    def GetImage(self):
        return self.capture.read()
                
    """画像ファイルの保存。"""
    def SaveImage(self, filename):
        ret, img = self.capture.read()
        if ret is False:
            rise("IO Error")
        cv2.imwrite(filename, img)
        
                 
#end of USBCamera Class