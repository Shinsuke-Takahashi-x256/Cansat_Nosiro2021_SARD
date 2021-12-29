# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 14:31:13 2021

@author: 高橋　辰輔
"""

def MakeFile(txt_PATH,w_data):
    fp = open(txt_PATH , "w")
    w_data = str(w_data)
    fp.writelines(w_data[1:len(w_data)-1:1])
    fp.close()

def WriteFile(txt_PATH,w_data):
    fp = open(txt_PATH , "a")
    w_data = str(w_data)
    fp.writelines(w_data[1:len(w_data)-1:1])
    fp.close()

def ReadFile(txt_PATH):
    txt_obj = open(txt_PATH , "r")
    txt_Array = txt_obj.read()
    txt_Array = txt_Array.split(",")
    txt_obj.close()
    return txt_Array