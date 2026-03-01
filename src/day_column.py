#!/usr/bin/env python3
from datetime import datetime, timedelta
from solar_time import calculate_true_solar_time

# 计算日柱
def calculate_day_column(true_solar_time):
    """
    计算日柱
    :param true_solar_time: 真太阳时（datetime对象）
    :return: 日柱（字符串）
    """
    # 规则1：23点后归属次日（命理核心规则）
    if true_solar_time.hour >= 23:
        calc_date = true_solar_time + timedelta(days=1)
    else:
        calc_date = true_solar_time
    
    # 规则2：直接使用兜底算法计算日柱
    # 由于zhdate库的限制，我们直接使用基准日偏移法
    return fallback_day_column(calc_date)

# 兜底算法：基准日偏移法
def fallback_day_column(calc_date):
    """
    兜底算法：使用基准日偏移法计算日柱
    :param calc_date: 计算日期（datetime对象）
    :return: 日柱（字符串）
    """
    # 60甲子表
    jia_zi = [
        '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
        '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
        '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
        '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
        '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
        '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'
    ]
    
    # 基准日期：1900-01-01 对应的日柱是 甲子
    base_date = datetime(1900, 1, 1)
    # 计算从基准日期到目标日期的天数
    delta_days = (calc_date - base_date).days
    
    # 基准日期对应的甲子索引（甲子是第0个）
    base_index = 0
    # 计算日柱索引
    day_index = (base_index + delta_days) % 60
    
    # 获取日柱
    return jia_zi[day_index]


