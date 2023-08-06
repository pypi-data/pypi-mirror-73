# -*- coding: utf-8 -*-

#实验效果：使用按钮控制LED模块亮度
#接线：使用windows或linux电脑连接一块arduino主控板，主控板D6接一个LED灯模块
import time
from pinpong.pinpong import PinPong,Pin,PWM #导入PWM类实现模拟输出

board = PinPong("uno")  #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno","COM36")  #windows下指定端口初始化
#board = PinPong("uno","/dev/ttyS1")   #linux下指定端口初始化

pwm0 = Pin(Pin.D6, Pin.PWM)
while True:
  for i in range(255): #从0到255循环
    pwm0.write_analog(i)  #设置模拟输出值
    print(i)
    time.sleep(0.05)
