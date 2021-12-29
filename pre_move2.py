# -*- coding: utf-8 -*-
"""
Created on Fri May 21 23:32:32 2021

@author: 高橋　辰輔
"""
import math
try:
    import File_lib
except:
    pass

try:
    import MPU_lib
except:
    pass

try:
    import BME820SP
except:
    pass
#気圧、温度

#高度センサーオフセット()

#開傘および着地衝撃[g]
#地上高度

def pre_main(sequence_count):
    TxtPATH = "premove_control_log.txt"
    try:
        File_lib.MakeFile(TxtPATH , 0)
    except:
        pass
    high_sta= [1023.5 , 0]
#当日気圧を入力
    high_offset = 0.3
    shock_sta = 3
    try:
        r_high = str(BME820SP.readData())
#        print(r_high)
    except:
        pass
    try:
        shock = MPU_lib.Get_Accel_status()
        shock_val = math.sqrt(shock[0]**2 + shock[1]**2 + shock[2]**2)
        shock_max = 0
        if shock_max < shock_val:
            shock_max = shock_val
    except:
        pass
        #testdata
    #    high = [1006.12 , 0]
    #    shock = [1,0,0]

    high = r_high.split(',')
#    print(high[1])
#    print(float(high[0]) >= float(high_sta[0]) and sequence_count == 0)
    if float(high[0]) >= float(high_sta[0]) and sequence_count == 0:
        sequence_count = 1
    elif float(high[0]) <= float(high_sta[0]) - high_offset and sequence_count == 1:
        sequence_count = 2
        #投下待ち
    elif float(high[0]) >= float(high_sta[0]) and sequence_count == 2:
        #and shock_max > shock_sta
        sequence_count = 3
    #投下判定１
    try:
        File_lib.WriteFile(TxtPATH , high + shock_val + shock_max)
    except:
        pass
    return sequence_count


if __name__ == '__main__':
    num = 10000
    sequence_count = 0
    while(num):
        sequence_count = pre_main(sequence_count)
        num -= 1
        print(sequence_count)
