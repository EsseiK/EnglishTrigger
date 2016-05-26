#!/usr/bin/python
#coding: UTF-8

import cv2
import cv2.cv as cv

import USBCamera
import GoogleCloudVision
import ImageDetectionResult

import datetime

"""　カメラ画像のキャプチャー。　"""
def takeAPicture(filename):

    _camera = USBCamera.USBCamera()
    _camera.SaveImage(filename)

    ret, image = _camera.GetImage()
    
    return image

"""　画像の表示。　"""
def showPicture(image):
    cv2.namedWindow("Capture", cv.CV_WINDOW_AUTOSIZE)
    cv2.imshow("Capture", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

"""　メイン関数。　"""
if __name__ == "__main__":

    # ファイル名の取得。
    now = datetime.datetime.today();
    datetimeStr = now.strftime("%Y%m%d_%H%M%S")    
    filename = "result/img_" + datetimeStr + ".jpg"

    # 画像の撮影。
    img = takeAPicture(filename)
    
    # 画像の解析。
    _vision = GoogleCloudVision.GoogleCloudVision()
    ret = _vision.ImageDetection(filename)

    # DEBUG:ローカルのJSONを使用。
#    f = open("result/img_20160522_055101.jpg.txt", "r")
#    ret = f.read();
#    f.close()

    f = open(filename + ".txt", "w")
    f.writelines(ret)
    f.close()

    # debug 
#    print(ret)
    _parser = ImageDetectionResult.ImageDetectionResult();
    _parser.ParseJson(ret)
    
    for data in _parser.Results:
        print data
    
    # DEBUG:画像の表示。
    # ※：何かしらのキー押下で終了。
    showPicture(img)

        
#    f = open(filename + ".txt", 'w')
#    f.writelines(ret)
#    f.close()