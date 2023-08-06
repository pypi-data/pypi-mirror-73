# -*- coding: utf-8 -*-

#实验效果：控制arduino UNO板载LED灯一秒闪烁一次
#接线：使用windows或linux电脑连接一块arduino主控板
import time
from pinpong.pinpong import PinPong,Pin

board = PinPong("leonardo")               #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno","COM36")      #windows下指定端口初始化
#board = PinPong("uno","/dev/ttyS1") #linux下指定端口初始化

led = Pin(Pin.D13, Pin.OUT) #引脚初始化为电平输出

while True:
  led.write_digital(1) #输出高电平
  time.sleep(1) #等待1秒 保持状态

  led.write_digital(0) #输出低电平
  time.sleep(1) #等待1秒 保持状态
