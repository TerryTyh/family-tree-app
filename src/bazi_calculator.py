#!/usr/bin/env python3
from datetime import datetime, timedelta
import math
import sys

# 导入各个模块
from solar_time import calculate_true_solar_time
from year_column import calculate_year_pillar
from month_column import calculate_month_pillar
from day_column import calculate_day_column
from time_column import calculate_time_column

# 计算生辰八字
def calculate_bazi(beijing_time, longitude=120.0):
    """
    计算生辰八字
    :param beijing_time: 北京时间（datetime对象）
    :param longitude: 出生地经度
    :return: 生辰八字（字符串）
    """
    # 1. 计算年柱（使用北京时间和经度）
    year_column = calculate_year_pillar(beijing_time, longitude)
    
    # 2. 计算月柱（使用北京时间和经度）
    month_column = calculate_month_pillar(beijing_time, longitude, year_column)
    
    # 3. 转换为真太阳时
    true_solar_time = calculate_true_solar_time(beijing_time, longitude)
    
    # 4. 计算日柱
    day_column = calculate_day_column(true_solar_time)
    
    # 5. 计算时柱
    time_column = calculate_time_column(true_solar_time, day_column[0])
    
    # 组合生辰八字
    return year_column + month_column + day_column + time_column

# 主函数
if __name__ == "__main__":
    # 交互式输入
    print("=== 生辰八字计算器 ===")
    time_str = input("请输入公历出生时间（格式：YYYY-MM-DD HH:MM:SS）：")
    longitude_str = input("请输入出生地经度（默认120.0）：")
    
    try:
        # 解析输入
        beijing_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        longitude = float(longitude_str) if longitude_str else 120.0
        
        # 计算生辰八字
        bazi = calculate_bazi(beijing_time, longitude)
        
        # 输出结果
        print(f"\n生辰八字: {bazi}")
    except Exception as e:
        print(f"错误: {e}")
