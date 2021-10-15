# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 15:26:49 2021

@author: 高橋　辰輔
"""

LEFT_TOP_M1 = 2 # lt 24
LEFT_TOP_M2 = 0 #23
RIGHT_TOP_M1 = 4 # rt 18
RIGHT_TOP_M2 = 5 #27
CAREER_CUT = 22 #6 pin31
#wiringpi pin number
running = 1
failed  = 0
sensor_health = {"BME280":failed,"GPS":failed,"MPU6250":failed,"AK8963":failed,"VL53L0x":failed,"picamera":failed}
module_health = {"numpy" :failed,"pre_move2":failed,"time":failed,"GPS_lib":failed,"MPU_lib":failed,"wiringpi":failed,"camera1":failed,"redcorn":failed}


try:
    import numpy
    module_health["numpy"] = running
except:
    module_health["numpy"] = failed

try:
    import pre_move2
    module_health["pre_move2"] = running
except:
    module_health["pre_move2"] = failed

try:
    import time
    module_health["time"] = running
except:
    module_health["time"] = failed

try:
    import GPS_GYSFDMAXB_lib
    module_health["GPS_lib"] = running
except:
    module_health["GPS_lib"] = failed

try:
    import MPU_lib
    MPU_lib.Set_Magnet_Cofigdata()
    module_health["MPU_lib"] = running
except:
    module_health["MPU_lib"] = failed

try:
    import wiringpi as wi
    module_health["wiringpi"] = running
    wi.wiringPiSetup()
except:
    module_health["wiringpi"] = failed

try:
    import camera1
    module_health["camera1"] = running
except:
    module_health["camera1"] = failed

try:
    import redcorn
    module_health["redcorn"] = running
except:
    module_health["redcorn"] = failed

print(module_health)
try:
    import File_lib
    File_lib.MakeFile("All_log.txt","_start_")
except:
    pass

try:
    import datetime
except:
    pass

def wi_wiringpi_setup():
    wi.pinMode( CAREER_CUT , 1)
    wi.pinMode( LEFT_TOP_M2, 1 )
    wi.pinMode( LEFT_TOP_M1, 1 )
    wi.pinMode( RIGHT_TOP_M1, 1 )
    wi.pinMode( RIGHT_TOP_M2, 1 )

def C_career_cut(status):
    wi.digitalWrite( CAREER_CUT , status)

def wi_motermode(LeftM1 , RightM1 , LeftM2 , RightM2, movetime):
    wi.wiringPiSetup()
    wi.digitalWrite(LEFT_TOP_M1,LeftM1)
    wi.digitalWrite(RIGHT_TOP_M1,RightM1)
    wi.digitalWrite(LEFT_TOP_M2,LeftM2)
    wi.digitalWrite(RIGHT_TOP_M2,RightM2)
    print(LeftM1,RightM1,LeftM2,RightM2,movetime,LEFT_TOP_M1,LEFT_TOP_M2,RIGHT_TOP_M1,RightM2)
    time.sleep(movetime)

def m_move(key , movetime):
#        print(key)
        if key == "w":
            wi_motermode(0,0,1,1 , 5)
            wi_motermode(0,0,0,0 , movetime)
        elif key == "d":
            wi_motermode(1,0,0,1 , 0.1)
            wi_motermode(0,0,1,1 , 5)
            wi_motermode(0,0,0,0 , movetime)
        elif key == "a":
            wi_motermode(0,1,1,0 , 0.1)
            wi_motermode(0,0,1,1 , 5)
            wi_motermode(0,0,0,0 , movetime)
        elif key == "s":
            wi_motermode(0,1,1,0 , 0.2)
            wi_motermode(0,0,0,0 , 0.5)
            wi_motermode(1,1,0,0 , 4)
            wi_motermode(0,0,0,0 , movetime)
        elif key == "n":
            wi_motermode(0,0,0,0 , movetime)
        else:
            return key , movetime

def ETM_enabletime_move(key , movetime):

        wi_motermode(0,0,0,0 , movetime)
#        print(key)
        if key == "w":
            print(key,movetime)
            wi_motermode(0,0,1,1 , movetime)
        elif key == "d":
            wi_motermode(1,0,0,1 , movetime)
            wi_motermode(0,0,1,1 , movetime)
        elif key == "a":
            wi_motermode(0,1,1,0 , movetime)
            wi_motermode(0,0,1,1 , movetime)
        elif key == "s":
            wi_motermode(0,1,1,0 , 0.3)
            wi_motermode(0,0,0,0 , 0.5)
            wi_motermode(1,1,0,0 , 3)
        elif key == "n":
            wi_motermode(0,0,0,0 , movetime)
        else:
            return key , movetime

#g = redcorn.main()
#cvプログラム名　現在未インストール
pro_count = "zero"
GPS_Realtime_txt_PATH  = "gps_realtime.txt"
GPS_Goalpoint_txt_PATH = "gps_goalpoint.txt"
All_Control_log_data = "All_log.txt"
sequence_count = 0

def pre_main():
    global sequence_count
    try:
        wi_wiringpi_setup()
    except:
        pass
    if sequence_count < 3:
        sequence_count = pre_move2.pre_main(sequence_count)
        pass
    elif sequence_count == 3:
        time.sleep(20)
        C_career_cut(1)
        time.sleep(3)
        C_career_cut(0)
        sequence_count = 4
        Moving_career_escape = ["w" , "a" , "d" , "s" , "w" , "a" , "d" , "s"]
        for i in Moving_career_escape:
            m_move(i,1)
            time.sleep(1)
            try:
                realtime = datetime.datetime.fromtimestamp(time.time())
                all_data = ["log_premove"]
                all_data.append(realtime.strftime('%H:%M:%S'))
                all_data.append(i)
                all_data.append("1")
                n = t_Writefile(All_Control_log_data, all_data)
                print(n)
            except:
                pass
def main():
    wi_wiringpi_setup()
    temp_a = 0
    temp_b = 0
    camera_sequence = []
    camera_count = 0
    move_count = 0
    GPS_Rt_Array = [0,0]
    goal_dicision = True
    move = ["w" , "1"]
    #初期値を前進にして機体進行方向とゴールとの角度を求める
    #初期ステータス決定
    global pro_count
    pro_count = "main"
    if module_health["GPS_lib"] == running:
        for i in range(3):
            GPS_GYSFDMAXB_lib.s_main()
        GPS_Ot_Array = u_OPENfile(GPS_Realtime_txt_PATH)
    #安定版ではコメントアウトしてください
    while(goal_dicision):
        if camera_count > 40:
            camera_count = 0
        #co = 0
        #while(GPS_Rt_Array[0] == [0] and co != 20):
        #    GPS_Rt_Array =)
        #time.sleep(0.05)
        #    co += 1
        #print(GPS_Rt_Array,"a")
        try:
            for i in range(3):
                if module_health["GPS_lib"] == running:
                    GPS_GYSFDMAXB_lib.s_main()
                elif module_health["GPS_lib"] != running:
                    pass
            GPS_Rtpre_Array = u_OPENfile(GPS_Realtime_txt_PATH)
            for i in range(3):
                if module_health["GPS_lib"] == running:
                    GPS_GYSFDMAXB_lib.s_main()
                elif module_health["GPS_lib"] != running:
                    pass
            GPS_Rtnow_Array = u_OPENfile(GPS_Realtime_txt_PATH)
            temp_a += (float(GPS_Rtnow_Array[0]) - float(GPS_Rtpre_Array[0]))
            temp_b += (float(GPS_Rtnow_Array[1]) - float(GPS_Rtpre_Array[1]))
            GPS_Rt_Array[0] = float(GPS_Rtnow_Array[0]) - temp_a
            GPS_Rt_Array[1] = float(GPS_Rtnow_Array[1]) - temp_b
            GPS_Gp_Array = u_OPENfile(GPS_Goalpoint_txt_PATH)
        #    print(GPS_Gp_Array , GPS_Rt_Array , GPS_Ot_Array)
        #要コメントアウト
            OR = x_Get_Distance(GPS_Rt_Array, GPS_Ot_Array)
            RG = x_Get_Distance(GPS_Gp_Array, GPS_Rt_Array)
        #OR,RGのベクトルを算出
            or_dis , or_rad = z_Get_Range_Angle(OR[0] , OR[1])
            rg_dis , rg_rad = z_Get_Range_Angle(RG[0] , RG[1])
        #OR,RGを極座標変換
        #print(or_dis , or_rad , rg_dis , rg_rad)
        except:
            move[0] = "goal"
            pass
        RT_rad = 0
        #ループ継続のため判定を反転
        if module_health["MPU_lib"] == running:
            Magnet_status = MPU_lib.Get_Magnet_status()
            RT_rad = s_atamawarui_hannbetuki(Magnet_status)
        elif module_health["MPU_lib"] != running:
            pass
        #print(RT_rad)
        out_re = [0,0]
        #try:
        for i in range(1):
            temp_move = y_Moving(or_rad , rg_rad , or_dis , rg_dis , RT_rad)
            move[0] = temp_move[0]
            move[1] = temp_move[1]
        #except:
        #    move[0] = "goal"
        if camera_count > 0:
            move[0] == "goal"
        m_move(move[0], move[1])
        #print(move)
        if move[0] == "goal":
            camera_count +=1
            threshold = 50
            camera1.ca_main()
            out_re= redcorn.re_main()
            camera_sequence.append("camera_count")
            camera_sequence.append(camera_count)
            camera_sequence.append("move_count")
            camera_sequence.append(move_count)
            #移動方向とゴール判定
            if out_re[0] == 0 and out_re[1] == 0 and camera_count == 0:
                ETM_enabletime_move( "w" , 2.5)
                t_data = ["w" , 2.5]
                camera_sequence.append( t_data )
            elif out_re[0] == 0 and out_re[1] == 0 and move_count == 0:
                ETM_enabletime_move( "a" , 0.2 )
                ETM_enabletime_move( "w" , 0.1 * i)
                t_data = ["a" , 0.2 , "w" , 0.1 * i]
                camera_sequence.append( t_data )
                move_count = 0
            elif out_re[0] != 0 and out_re[1] != 0 and move_count < 14:
                if out_re[0] < (320 - threshold):
                    ETM_enabletime_move("a", 0.05)
                    ETM_enabletime_move( "n" , 0.08 )
                    t_data = [ "a", 0.05 , "n" , 0.08 ]
                    camera_sequence.append( t_data )
                elif out_re[0] > (320 + threshold):
                    ETM_enabletime_move("d", 0.05)
                    ETM_enabletime_move( "n" , 0.08 )
                    t_data = ["d", 0.05 ,  "n" , 0.08 ]
                    camera_sequence.append( t_data )
                else:
                    ETM_enabletime_move( "w" , 0.8 )
                    ETM_enabletime_move( "n" , 0.08 )
                    t_data = ["w" , 0.5 , "n" , 0.08 ]
                    camera_sequence.append( t_data )
                    move_count += 1
                    print("move_count += 1")
            elif out_re[0] != 0 and out_re[1] != 0 and move_count > 14:
                print("Hello,world")
                goal_dicision = False
                #ETM_enabletime_move("n",32767)
            else:
                break
        GPS_Ot_Array = GPS_Rt_Array
        #実行結果
        #(['45.379778333333334', ' 141.00000003207165'], ['42.38133166666667', ' 141.000000036105'])
        #(0.0, 2.9984466666666663, True)
        #Hello,world
        #try:
        for i in range(1):
            realtime = datetime.datetime.fromtimestamp(time.time())
            all_data = ["log"]
            all_data.append(realtime.strftime('%H:%M:%S'))
            all_data.append(realtime.strftime('%H:%M:%S'))
            if module_health["GPS_lib"] == running:
                for i in GPS_Rt_Array:
                    all_data.append(i)
            if module_health["MPU_lib"] == running:
                for i in Magnet_status:
                    all_data.append(i)
            for i in out_re:
                all_data.append(i)
            for i in camera_sequence:
                all_data.append(i)
            for i in move:
                all_data.append(i)
            n = t_Writefile(All_Control_log_data, all_data)
            print(n)
            all_data.clear()
            camera_sequence.clear()
        #except:
        #    pass
        #要コメントアウト

def s_atamawarui_hannbetuki(data):
    #ばなな
    offset = [-145.518, 84.425, 72.759]
    for l in range(3):
        data[l] -= offset[l]
    # N , E , S , W
    #n4 e3 s2 w1
    hougaku = [ 4 , 3 , 2 , 1]
    #N--3.6839999999999975, -10.131, 123.10699999999999]
    #E-151.765, 164.594, 144.948
    #S-208.867, 130.824, 150.47400000000002
    #E-181.851, 81.70400000000001, 145.562
    x_sta = [-3,  -49 , -60,  -25]
    y_sta = [-10 , -43 , 0 , 37]
    z_sta = [123 , 115 , 95 , 110]
    score = [0 , 0 , 0 , 0]
    for k in range(4):
        xc = (data[0] - x_sta[k]) **2
        yc = (data[1] - y_sta[k]) **2
        zc = (data[2] - z_sta[k]) **2
        score[k] = xc + yc + zc
    out_d = hougaku[score.index(min(score))]
    return out_d

def t_Writefile(txt_PATH , w_data):
    global pro_count
    pro_count = "u"
    #安定版ではコメントアウトしてください
    fp = open(txt_PATH , "a")
    w_data = str(w_data)
    fp.writelines(w_data[1:len(w_data)-1:1])
    fp.writelines("\n")
    fp.close()
    return w_data

def u_OPENfile(txt_PATH):
    global pro_count
    pro_count = "u"
    #安定版ではコメントアウトしてください
    txt_obj = open(txt_PATH , "r")
    txt_Array = txt_obj.read()
    txt_Array = txt_Array.split(",")
    txt_obj.close()
    return txt_Array

def x_Get_Distance(GPS_B_Array ,  GPS_A_Array):
    global pro_count
    pro_count = "x"
    #安定版ではコメントアウトしてください
    #ABvector
    la = 0
    lo = 1
    GPS_la_Distance = float(GPS_B_Array[la]) - float(GPS_A_Array[la])
    GPS_lo_Distance = float(GPS_B_Array[lo]) - float(GPS_A_Array[lo])
    return GPS_la_Distance , GPS_lo_Distance

def z_Get_Range_Angle(GPS_la_Distance , GPS_lo_Distance):
#    print(GPS_la_Distance , GPS_lo_Distance , "dis")
    r_dis = numpy.sqrt(GPS_la_Distance * GPS_la_Distance + GPS_lo_Distance * GPS_lo_Distance)
    #rad = numpy.arctan2(GPS_la_Distance , GPS_lo_Distance)
    GPS_la_two_Distance = GPS_la_Distance ** 2
    GPS_lo_two_Distance = GPS_lo_Distance ** 2
    #n4 e3 s2 w1
#    print(GPS_la_two_Distance , GPS_lo_two_Distance)
    if GPS_la_Distance > 0 and  3.5 *GPS_lo_two_Distance <= GPS_la_two_Distance:
        rad = 4
    elif GPS_lo_Distance > 0 and GPS_la_two_Distance <= 3.5 * GPS_lo_two_Distance:
        rad = 3
    elif GPS_la_Distance <= 0 and 3.5 * GPS_lo_two_Distance <= GPS_la_two_Distance:
        rad = 2
    elif GPS_lo_Distance <= 0 and GPS_la_two_Distance <=  3.5 * GPS_lo_two_Distance:
        rad = 1
#    print(r_dis , rad , "out")
    return r_dis , rad

def y_Moving(or_rad , rg_rad , or_dis , rg_dis , RT_rad):
    if RT_rad != 0 and 2e-5 < rg_dis:
        rad = RT_rad
    else:
        rad = or_rad
    #x軸からの角度、センサーが壊れた場合に備えて上の計算式もバックアップとして読み出せるようにしとく
    if  rg_dis <= 1e-3:
        movemode = "goal"
#    elif 15e-5 < rg_dis and or_dis < 1e-7:
#        movemode = "s"
    elif rad == rg_rad:
        movemode = "w"
        movetime = rg_dis / or_dis * 10 +1
    elif rg_rad - rad == 1 or rg_rad - rad == -3:
        movemode = "a"
    elif rg_rad - rad == -1 or rg_rad - rad == 3:
        movemode = "d"
    else:
        movemode = "a"
    movetime = 1
    return movemode, movetime
    #画像認識や距離センサーの見地範囲外でゴール判定してしまった場合ミッションが終わるのでセンサーが決定し次第修正!!!!!!\

if __name__ == '__main__':
    sequence_count = 4
    while(True):
        if sequence_count < 4:
            pre_main()
            time.sleep(0.05)
            print(sequence_count)
        if sequence_count == 4:
            print(sequence_count)
            main()

#メイン処理
