# HITSZ课表转换工具

## 介绍

目前HITSZ助手似乎不支持研究生课表的Excel导入。
本项目的目标是能够将HITSZ Excel格式的课表转换
为任意课程APP可导入的格式。

## 基本使用方式
安装下述依赖:
```shell
pip install parse 
pip install pandas
pip install xlrd
```

运行: 
```shell
# python ./wakeup-coverter.py [你的Excel课表路径] [生成的路径(后缀.csv)] 
python ./wakeup-coverter.py ./courses/HITSZ-master-template.xlsx ./courses/wakeup-format.csv 
```

## 支持

目前仅支持的课表程序APP:

- WakeUp课程表

- ... (TODO)

## 架构

工具目前较为简单，有需求可以进一步迭代