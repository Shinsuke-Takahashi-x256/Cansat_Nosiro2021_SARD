# -*- coding: utf-8 -*-
import time
import picamera #カメラモジュール用
import cv2 as cv

def ca_main():
    # カメラ初期化
    camera  = picamera.PiCamera()
    # 解像度の設定
    camera.resolution = (640, 480)
    # 撮影の準備
    camera.start_preview()
    # 準備している間、少し待機する
    time.sleep(0)
    # 撮影して指定したファイル名で保存する
    camera.capture('redcorn1.jpg')
    camera.stop_preview()
    camera.close()

if __name__ == '__main__':
    ca_main()
