# -*- coding:utf-8 -*-
'''
@Author: Scfan
@Date: 2018-12-06 15:03:37
@LastEditors: Scfan
@LastEditTime: 2018-12-24 21:56:05
@Description: 工作&amp;学习&amp;生活
@Email: 643566992@qq.com
@Company: 上海
@version: V1.0
@Msg:
    二维码 生成、读取 等
'''

import qrcode 
img = qrcode.make('Some data here') 
img.save("test.png") 

高级使用

import qrcode # 导入模块
qr = qrcode.QRCode(
  version=1,
  error_correction=qrcode.constants.ERROR_CORRECT_L,
  box_size=10,
  border=4,
)
qr.add_data('Some data')
qr.make(fit=True)
img = qr.make_image()
img.save("advanceduse.png")

version：值为1~40的整数，控制二维码的大小（最小值是1，是个21×21的矩阵）。 如果想让程序自动确定，将值设置为 None 并使用 fit 参数即可。
error_correction：控制二维码的错误纠正功能。可取值下列4个常量：
    ERROR_CORRECT_L 大约7%或更少的错误能被纠正
    ERROR_CORRECT_M （默认）大约15%或更少的错误能被纠正
    ERROR_CORRECT_Q 大约25%或更少的错误能被纠正
    ERROR_CORRECT_H.大约30%或更少的错误能被纠正
box_size：控制二维码中每个小格子包含的像素数。
border：控制边框（二维码与图片边界的距离）包含的格子数（默认为4，是相关标准规定的最小值）

QRCode官网https://pypi.python.org/pypi/qrcode
class QrCode():

    def __init__():
        pass
    
    def main(self):
        pass


if __name__ == '__main__':
    pass
