#coding=utf-8
'''
Author  :SongBaoBao
Project :new 
FileName:setup.py
Currtime:2020/7/6--01:54
Commpany:Tsinghua University
MyCsdnIs:https://blog.csdn.net/weixin_43949535
MyLolLpl:Royal Never Give Up
'''
# 
# 
# 
from distutils.core import setup
setup(
name='thefirstmodule', # 对外我们模块的名字
version='1.0', # 版本号
description='这是第一个对外发布的模块，测试哦', #描述
author='songbaobao', # 作者
author_email='songbaobao@163.com',
py_modules=['thefirstmodule.demo1'] # 要发布的模块
)