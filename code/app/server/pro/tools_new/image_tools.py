#! -*- coding:utf-8 -*-
u"""
    Image 处理 图片处理工具

Image_Tools
- image2text            图片转文字 文字识别
- image2blackwhite      图片转黑白图 
- image2ascii           图片转ASCII图形
- image_del_watermark   图片去水印

# 安装
pip install PIL pillow tesseract pytesseract numpy
"""

import sys, random, argparse
import numpy as np    
import math

import pytesseract
from PIL import Image
import os
import copy

class Image_Tools(object):
    """
        Image Tools 图片处理工具
    """
    def __init__(self,*args,**kwargs):
        # 参数配置
        filepath = kwargs.get('filepath')
        if not filepath:
            logging.error('>> 文件路径[%s]不存在,请重新输入'%filepath)

        self.image = self.image_open(filepath)

    def _setup(self,image=None):
        u" 函数初始处理 "
        return image or self.image
    def _teardown(self,image=None):
        u" 函数结束处理 "
        self.image = image or self.image

    #######################
    # 常用API
    #######################

    def image2text(self,image=None,lang='chi_sim'):
        u""" 图片转文字 文字识别
        @param image: 图片对象
        @param lang: 图片识别的语言
        Python3 OCR，即Optical Character Recognition，光学字符识别
        """
        image = self._setup(image)
        # 函数处理
        langs_dic = {
            'chi_sim':'中文',
            'eng':'英文/阿拉伯字母'
        }
        lang = lang if lang in langs_dic.keys() else 'chi_sim'
        text = pytesseract.image_to_string(image,lang=lang)

        self._teardown(image)
        return text

    def image2blackwhite(self,image=None,filepath="a.png"):
        u""" 图片转黑白图
        @param image: 图片对象
        """
        image = self._setup(image)
        width,height = image.size
        fazhi=25
        # 遍历像素点
        for x in range(width):
            for y in range(height):
                if (image.getpixel((x,y))[0]<fazhi)|(image.getpixel((x,y))[1]<fazhi)|(image.getpixel((x,y))[2]<fazhi):
                    image.putpixel((x,y),(0,0,0)) # 置为黑点
                else:
                    image.putpixel((x,y),(255,255,255)) # 置为白点
        for x in range(width):
            for y in range(height):
                image.getpixel((x,y)) # 置为黑点
                break
        
        image.show()
        image.save(filepath)

    def image2ascii(self,image=None,scale=0.43,cols=80,outFile='out.txt',moreLevels=True):
        u""" 图片转ASCII图形
        @param image: 图片对象
        @param scale: 垂直比例系数测试得0.43效果佳，必须用等长字体显示文本，如宋体、Courier
        @param cols: 默认分割的列数，列数越大精细度越大，但不建议过大
        @param outFile: 输出文本文件
        @param moreLevels: 灰度级别
        # 图片转ASCII的基本原理是将灰度图片分割成众多小网格，将小网格的平均亮度计算出来用不同亮度字符代替
        # 灰度梯度对应字符可参考：http://paulbourke.net/dataformats/asciiart/

        """
        image = self._setup(image)
        # 70级灰度梯度（越来越亮）
        gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        # 10级灰度梯度
        gscale2 = '@%#*+=-:. '

        # 计算每一小块平均亮度
        def getAverageL(image):
            im = np.array(image)#小块转成二维数组
            w, h = im.shape#保存小块尺寸
            return np.average(im.reshape(w * h))#将二维数组转成一维，求均值
        
        #根据每一小块平均亮度匹配ASCII字符
        image = image.convert('L')#打开图片并转换成灰度图
        W, H = image.size[0], image.size[1]#保存图像宽高
        print("图像宽高: %dx%d" % (W, H))
        w = W / cols#计算小块宽度
        h = w / scale#计算小块高度，此处除垂直比例系数用于减少图像违和感，经测试scale为0.43时效果较好
        rows = int(H / h)#计算行数
        print("共有%d行 %d列小块" % (rows,cols))
        print("每一小块宽高: %dx%d" % (w, h))

        #图像太小则退出
        if cols > W or rows > H:
            print("图像太小不足分割！（提高图像分辨率或降低精细度）")
            exit(0)

        aimg = []#文本图形存储到列表中
        #逐个小块匹配ASCII
        for j in range(rows):
            y1 = int(j * h)#小块开始的y坐标
            y2 = int((j + 1) * h)#小块结束的y坐标
            if j == rows - 1:
                y2 = H#最后一个小格不够大，结束y坐标用图像高度H表示
            aimg.append("")#先插入空串
            for i in range(cols):
                x1 = int(i * w)#小块开始的x坐标
                x2 = int((i + 1) * w)#小块结束的x坐标
                if i == cols - 1:
                    x2 = W#最后一个小格不够大，结束x坐标用图像宽度W表示
                img = image.crop((x1, y1, x2, y2))#提取小块
                avg = int(getAverageL(img))#计算平均亮度
                if moreLevels:
                    gsval = gscale1[int((avg * 69) / 255)]#平均亮度值[0,255]对应到十级灰度梯度[0,69]，获得对应ASCII符号
                else:
                    gsval = gscale2[int((avg * 9) / 255)]#平均亮度值[0,255]对应到七十级灰度梯度[0,9]，获得对应ASCII符号
                aimg[j] += gsval#更新文本图形

        f = open(outFile, 'w')#保存文档图片
        for row in aimg:
            f.write(row + '\n')
        f.close()
        print("ASCII文本图形存储于%s" % outFile)

    def image_del_watermark(self,sourcePic,watermarkPic,outPic):
        u""" 图片去水印
        @param sourcePic: 源图片路径
        @param watermarkPic: 水印图片路径
        @param outPic: 输出图片路径
        使用说明:

            参数说明:
            - 原图片 1.png
            - 图片备份 1_bak.png
            - 将所有 水印图片 粘贴复制到 (含空白+水印颜色) s.png
            - 输出图片 2.png

            使用步骤:
            - word文档 另存为 html  (得到html+图片文件夹)
            - 准备好水印图片 (粘贴复制所有水印) > s.png
            - img_get_rgb("s.png") 获取水印的颜色区间
            - img_rgb_deal(filename,output_name,rgb_data) 去除图片水印
            - 将图片文件夹中的所有图片替换掉,html使用word打开,另存为word即可。

        TODO:
        1. 代码思路:
            1. 获取所有水印的像素点,
            2. 获取图片的所有像素点,
            3. 剔除图片中水印的像素点
        2. 存在不足:
            1. 会去除 和水印颜色相同非水印内容
            2. 水印像素点 无法精准识别 需要像素偏移值 deviation_num
        """
        def img_get_rgb(file_name,txt_name='1.txt',deviation_num=2):
            u"""
                获取 水印图片 所有像素值
                @param file_name: 文件名称
                @param txt_name: 保存 水印像素点文件名称
                @param deviation_num: 像素偏移值
            """
            i = 1; j = 1
            img = Image.open(file_name)
            print("图片 名称:[%s] 大小: [%s:%s]"%(file_name,img.size[0],img.size[1]))

            rows = []
            width = img.size[0]
            height = img.size[1]
            for i in range(0,width):
                for j in range(0,height):
                    data = img.getpixel((i,j))
                    tmp = list(data)
                    tmp.append(255)
                    tmp = tuple(tmp)
                    rows.append(tmp)
            rows = list(set(rows))

            # 水印颜色点 额外处理
            new_rows = list()
            for row in rows:
                # 去除 黑色点
                if row == (0, 0, 0, 255):
                    continue

                # 存在所截水印图片未完全去除水印 需要增加 像素偏移值
                # 额外增加 像素偏移值       TODO 此方法会删除部分无法删除的水印,也可能删除有效数据
                for x in range(0,deviation_num+1):
                    for y in range(0,deviation_num+1):
                        for z in range(0,deviation_num+1):
                            row = (abs(row[0]-x),abs(row[1]-y),abs(row[2]-z),255)
                            new_rows.append(row)

                new_rows.append(row)
            rows = copy.deepcopy(new_rows)

            # 保存 水印像素点
            os.system('rm -f %s'%txt_name)
            with open(txt_name,'wb') as f:
                for row in rows:
                    f.write(str(row)+"\n")

            return rows
            # sort -n 1.txt | uniq

        def img_rgb_deal(filename,output_name,rgb_data=[(255,255,255,255)]):
            u"""
                去除图片中指定 RGB 像素点
                关键点:
                    1. 水印 像素非准确点 都是像素区间
                    2. rgb_data [(),()] 其内为元组

                @param filename: 输入文件名称
                @param output_name: 输出文件名称
                @param rgb_data: 水印的 RGB 颜色列表
            """

            i = 1; j = 1
            img = Image.open(filename)
            width,height = img.size
            print("图片 名称:[%s] 大小: [%s:%s]"%(filename,img.size[0],img.size[1]))

            for i in range(0,width):
                for j in range(0,height):
                    # 打印该图片的所有点
                    data = (img.getpixel((i,j)))

                    #if data[0] in range(200,256) and data[1] in range(200,256) and data[2] in range(200,256):
                    #    img.putpixel((i,j),(255,255,255,255))

                    if data in rgb_data:
                        # 重置为 白色
                        img.putpixel((i,j),(255,255,255,255))

            # 把图片强制转成RGB
            img = img.convert("RGB")
            img.show()
            # 保存修改像素点后的图片
            if os.path.exists(output_name):
                os.system('rm -f %s'%output_name)
            img.save(output_name)

        watermarkPic="../statics/images/s.png"
        sourcePic="../statics/images/1.png"
        outPic ="../statics/images/2.png"
        # 获取 水印图片 像素点 区间
        rgb_data = img_get_rgb(watermarkPic)
        print rgb_data
        img_rgb_deal(filename=sourcePic,output_name=outPic,rgb_data=rgb_data)

    def image_save(self,image,file_path):
        u""" 图片保存
        """
        image.save(file_path)

    def image_open(self,file_path,*args,**kwargs):
        u""" 打开图片
        """
        return Image.open(file_path)

    #######################
    # 基础API - 不常用
    #######################

    
    def image_convert(self,image,tran_type='jpeg'):
        u""" 图片格式转换
    
        """
        image_rgb = image.convert('RGB')
        image_rgb.save('tmp2.jpg','jpeg')
        return 

    def image_infos(self,image):
        u""" 获取图片各种信息
        """
        # 长宽
        
        print image.size

    def image_cut(self,image,sizes=(0,0),dtype='ANTIALIAS'):
        u""" 图片切割
        """
        half_size = (image.size[0]/2,image.size[1]/2)
        # 只适合等比例切割
        image.thumbnail(half_size,Image.ANTIALIAS) 
        # 过滤器类型
        # Image.NEAREST,Image.BILINEAR,Image.BICUBIC,Image.ANTIALIAS
        # 适合不等比例切割
        image_resize = image.resize((image.size[0],image.size[1]*2),Image.ANTIALIAS)

    def image_filter(self):
        # 过滤
        crop_rect = (0,100,200,100)
        image_crop = image.crop(crop_rect)
        
        buffer = []
        for pixel in image.getdata():
            buffer.append((255-pixel[0],255-pixel[1],255-pixel[1]))
        
        # 像素反转
        image.putdata(buffer)

if __name__ == '__main__':
    image_tools = Image_Tools(filepath='../tmp/tmp.png')
    #image_tools.image2text()
    image_tools.image2blackwhite()
    image_tools.image2ascii()

