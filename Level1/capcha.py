#!/usr/bin/python
#coding=utf-8
"""
*文件说明:captha.py
*作者:高小调
*创建时间:2017年09月09日 星期六 22时35分43秒
*开发环境:Kali Linux/Python v2.7.13
"""
from PIL import Image
import hashlib
import time
import os
#对验证码进行切割
def cut(img):
    #打开原验证码文件
    im = Image.open(img)
    #进行灰度化
    im_new = im.convert('L')
    #进行切割
    for i in range(4):
        x = i*10
        y = 0
        m = hashlib.md5()
        m.update("%s%d"%(time.time(),i))
        im_tmp = im_new.crop((x,y,x+6,im_new.size[1]))
        im_tmp.save("icoset/%s.jpg"%(m.hexdigest()))
def cut_all():
    for i in range(1,101):
        img = "Imgs/%d.jpg"%(i)
        cut(img)
    print "验证码切割完成!"

#获取图片特征值
def get_feature(img):
    width,height = img.size
    pixel_list = [] 
    for y in range(height):
        pix_x = 0
        for x in range(width):
            if img.getpixel((x,y)) == 0:
                pix_x += 1
        pixel_list.append(pix_x)
    
    for x in range(width):
        pix_y = 0
        for y in range(hight):
            if img.getpixel((x,y)) == 0:
                pix_y += 1
        pix_list.append(pix_y)
    return pixel_list

def get_bin_table(threshold=140):
    table = []
    for i in range(256):
        if i < threshold : 
            table.append(0)
        else:
            table.append(1)
    return table

def get_matrix(img):
    imgry = img.convert('L')
    table = get_bin_table()
    out = imgry.point(table,'1')
    for i in range(out.size[0]):
        for j in range(out.size[1]):
            table.append(out.getpixel((i,j)))
    return table;

def init():
    matrix = []
    for i in range(10):
        img = Image.open("icoset/%d.jpg"%(i))
        matrix.append(get_matrix(img))
    return matrix

def identify(img,matirx):
    img = img.convert("L")
    imgs = []
    #切割
    for i in range(4):
        x = i*10
        y = 0
        m = hashlib.md5()
        m.update("%s%d"%(time.time(),i))
        im_tmp = img.crop((x,y,x+6,img.size[1]))
        imgs.append(im_tmp)
    #二值化
    _matrix = []
    for i in range(4):
        _matrix.append(get_matrix(imgs[i]))
    #对比
    ret = []
    for i in range(4):
        for j in range(10):
            if _matrix[i] == matirx[j]:
                ret.append(j)
    print ret

def main():
    matrix = init()
    img = Image.open("test.jpg")
    identify(img,matrix)
    '''
    for i in range(1,10):
        img = Image.open("Imgs/%d.jpg"%(i))
        identify(img,matrix)
    '''
main()

