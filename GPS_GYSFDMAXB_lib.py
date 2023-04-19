# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 14:18:09 2021

@author: 高橋　辰輔
"""
#OSのレベルで並列実行してファイルに常に最新のものが保存されるようにして
#データ取得時までの時間別のプログラムを実行できるようにしてる。
import serial
import sys

import time

pro_count = "zero"
UART_PATH = '/dev/serial0'
#
GPS_Realtime_txt_PATH = "gps_realtime.txt"

#Testdata

def s_main():
    global pro_count
    global GPS_Realtime_txt_PATH
    pro_count = "main"
    Main_State = 0
    #安定版ではコメントアウトしてください
    GPS_raw_Array = i_GPS_UART_getval()
#    print(GPS_raw_Array)
    GPS_Array = r_NMEA_Decorder(GPS_raw_Array)
#    print(GPS_Array)
    #緯度経度の情報のみ
    if GPS_Array != 0:
        Main_State = t_TXT_Write_module(GPS_Array,GPS_Realtime_txt_PATH)
    return Main_State


def i_GPS_UART_getval():
    #
    global pro_count
    global UART_PATH
    pro_count = "i"
    #安定版ではコメントアウトしてください
    ser = serial.Serial(UART_PATH,9600,timeout = 0.5)
    Data = ser.readline()
    Data = str(Data)
    Data = Data[1:len(Data)]
    time.sleep(0.1)
    GPS_Array = Data.split(',')
    return GPS_Array

def r_NMEA_Decorder(GPS_Array):
    global pro_count
    pro_count = "r"
    #安定版ではコメントアウトしてください
    DataType = 0
    GGA_DMM_latitude = 2
    GGA_DMM_longitude = 4
    lalo = [0,0]
    if GPS_Array[DataType] == "'$GPGGA":
        lalo[0] = sub_s_DD_DMM_converter_la(GPS_Array[GGA_DMM_latitude])
        lalo[1] = sub_s_DD_DMM_converter_lo(GPS_Array[GGA_DMM_longitude])

#        GPS_Array_a = list(GPS_Array[GGA_DMM_latitude])

#        GPS_Array_a[0] = " "
#        GPS_Array_a[1] = " "
#        GPS_Array_a[len(GPS_Array_a)-1] = " "
#        GPS_Array_a[len(GPS_Array_a)-2] = " "
#        GPS_Array_b = list(GPS_Array[GGA_DMM_longitude])
#        print(GPS_Array_a)
#        GPS_Array_b[0] = " "
#        GPS_Array_b[1] = " "
#        GPS_Array_b[len(GPS_Array_b)-1] = " "
#        GPS_Array_b[len(GPS_Array_b)-2] = " "

#        print(GPS_Array_b)
#        lalo[0] = sub_s_DD_DMM_converter(''.join([str(i) for i in GPS_Array_a]))
#        lalo[1] = sub_s_DD_DMM_converter(''.join([str(i) for i in GPS_Array_b]))
    if lalo[0] != 0 and lalo[1] != 0:
        return lalo
    return 0

def sub_s_DD_DMM_converter_la(DMM_val):
    #
    global pro_count
    pro_count = "s"
    #安定版ではコメントアウトしてください
    y_DD = 0
    if DMM_val != "":
        DMM_val = float(DMM_val)/100
        DMM_val = round(DMM_val , 6)
        y_str = str(DMM_val)
#        print(y_str,"a")
        #y_float = float(DMM_val/100)
        y_min = float(y_str[3:len(y_str):1])/60*100 / 1e6
        #IMPORTANT::NMEAのGGAはDMM系!!
#        print(len(y_str))
        if len(y_str) != 9:
            y_min *= 10
#        print(y_min , "n")
        y_DD  = float(y_str[0:3:1]) + y_min
        y_DD = round(y_DD , 5)
    return y_DD
    #print(y_min)
    #print(y_DD)

def sub_s_DD_DMM_converter_lo(DMM_val):
    #
    global pro_count
    pro_count = "s"
    #安定版ではコメントアウトしてください
    y_DD = 0
    if DMM_val != "":
        DMM_val = float(DMM_val)/100
        DMM_val = round(DMM_val , 7)
        y_str = str(DMM_val)
#        print(y_str,"a")
        #y_float = float(DMM_val/100)
        y_min = float(y_str[4:len(y_str):1])/60*100 / 1e6
#        print(len(y_str))
        if len(y_str) != 10:
            y_min *= 10
        #IMPORTANT::NMEAのGGAはDMM系!!
#        print(y_min , "n")
        y_DD  = float(y_str[0:3:1]) + y_min
        y_DD = round(y_DD , 5)
    return y_DD
    #print(y_min)
    #print(y_DD)

def t_TXT_Write_module(GPS_Array,GPS_txt_PATH):
    if GPS_Array != 0:
        fp = open(GPS_txt_PATH , "w")
        GPS_Array = str(GPS_Array)
        fp.writelines(GPS_Array[1:len(GPS_Array)-1:1])
        fp.close()
    return GPS_Array


if __name__ == "__main__":
    GPS_Realtime_txt_PATH = "gps_goalpoint.txt"
    #実行モードが本プログラムだけの時ゴール地点の座標を取得し出力するモードに
    i = 1000
    try:
        while(True):
            #print(i_GPS_UART_getval())
            print(s_main())
            i-=1
            time.sleep(0.1)
    except KeyboardInterrupt:
        sys.exit("KeyboardInterrupt")
