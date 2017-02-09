# Discovery

> Data explorer  
> Input : Data  
> Output : Report

## Dependency

python >= 3.3  
numpy  
scipy   
pandas  
matplotlib  
Jinja  
weasyPrint  
[report website](http://pbpython.com/pdf-reports.html)

## Data Type

时间序列数据：time series data  
截面数据：cross section data  

## Statistics

### 概览信息表 :  

特征数量总数（环图），分类变量和数值变量占比  
所有特征的名称（可跳转至详细信息），基本统计数据（总数，均值，中位数，方差，最大值，最小值，缺失度，数据类型，unique）

### 概览信息图 : 
 
#### 截面数据

所有（unique > 10）特征的直方图（一张大图内套小图，能一眼看清所有特征的大致分布）  
所有（unique < 10）特征的饼图

#### 时间序列数据

所有（unique > 10）特征的折线图  
所有（unique < 10）特征的饼图

### 特征详细信息 :  

#### 截面数据

当前特征的均值，中位数，方差，最大值，最小值，四分位数  
当前特征的直方图/饼图（根据unique决定），图中标注均值，中位数，方差，并划分2σ  
当前特征与其他特征的相关性情况 :  
	1. 相关性列表，特征名、相关系数、p值（排序后只列举相关系数大于+-0.5的部分，及p值）  
	2. 散点图（二维，x轴为当前特征，y轴为相关特征，标明相关系数及p值）  
特征在分类特征下的均值/方差分析 :  
	1. 均值/方差分析表，特征名，分类特征，均值/方差分析,p值  
	2. 分类直方图（单图多表，标明特征名，分类名，均值/方差，p值）

#### 时间序列数据

当前特征的均值，中位数，方差，最大值，最小值，四分位数  
当前特征的折线图/饼图（根据unique决定）