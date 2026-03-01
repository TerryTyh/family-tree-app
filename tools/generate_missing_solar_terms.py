#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成缺失年份的节气数据并存储到数据库
"""

import sqlite3
import datetime
import math
import sys
import os
from datetime import datetime, timedelta

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')

from solar_time import calculate_true_solar_time
from check_solar_terms_db import check_db_years, find_missing_years

# 数据库文件路径
import os
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'solar_terms.db')

# 十二节气名称（按顺序）
SOLAR_TERMS = [
    "小寒", "大寒", "立春", "雨水", "惊蛰", "春分",
    "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
    "小暑", "大暑", "立秋", "处暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]

# 节气太阳黄经（度）
SOLAR_TERMS_DEGREES = [
    285, 300, 315, 330, 345, 0,
    15, 30, 45, 60, 75, 90,
    105, 120, 135, 150, 165, 180,
    195, 210, 225, 240, 255, 270
]

# 从solar_terms_db导入计算函数
from solar_terms_db import calculate_year_solar_terms

# 生成并存储缺失年份的节气数据
def generate_missing_terms():
    """
    生成缺失年份的节气数据并存储到数据库
    """
    # 获取已有的年份
    db_years = check_db_years()
    print(f"数据库中已有{len(db_years)}个年份的数据")
    
    # 找出缺失的年份（处理1900-2100年）
    missing_years = find_missing_years(1900, 2100, db_years)
    print(f"需要生成{len(missing_years)}个年份的节气数据")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    total_count = 0
    success_count = 0
    error_count = 0
    
    print("开始生成缺失年份的节气数据...")
    
    for year in missing_years:
        print(f"处理年份: {year}")
        
        try:
            # 计算该年份所有节气的北京时间
            solar_terms_bt = calculate_year_solar_terms(year)
            
            # 计算不同经度的真太阳时
            longitudes = [120.0, 116.4, 120.19, 102.73]  # 包含测试用例中使用的经度
            for longitude in longitudes:
                for term_name, bt in solar_terms_bt.items():
                    # 计算真太阳时
                    true_solar = calculate_true_solar_time(bt, longitude)
                    
                    # 存储到数据库
                    cursor.execute('''
                    INSERT OR REPLACE INTO solar_terms (year, term_name, bt_datetime, longitude, true_solar_datetime)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (year, term_name, bt.isoformat(), longitude, true_solar.isoformat()))
                    
                    total_count += 1
                    success_count += 1
        except Exception as e:
            print(f"处理年份{year}时出错: {str(e)}")
            error_count += 1
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\n生成完成")
    print(f"总处理: {total_count}")
    print(f"成功: {success_count}")
    print(f"失败: {error_count}")

# 重新生成指定年份的节气数据
def regenerate_terms_for_years(years):
    """
    重新生成指定年份的节气数据
    :param years: 要重新生成的年份列表
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    total_count = 0
    success_count = 0
    error_count = 0
    
    print(f"开始重新生成指定年份的节气数据...")
    
    for year in years:
        print(f"处理年份: {year}")
        
        try:
            # 计算该年份所有节气的北京时间
            solar_terms_bt = calculate_year_solar_terms(year)
            
            # 计算不同经度的真太阳时
            longitudes = [120.0, 116.4, 120.19, 102.73]  # 包含测试用例中使用的经度
            for longitude in longitudes:
                for term_name, bt in solar_terms_bt.items():
                    # 计算真太阳时
                    true_solar = calculate_true_solar_time(bt, longitude)
                    
                    # 存储到数据库
                    cursor.execute('''
                    INSERT OR REPLACE INTO solar_terms (year, term_name, bt_datetime, longitude, true_solar_datetime)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (year, term_name, bt.isoformat(), longitude, true_solar.isoformat()))
                    
                    total_count += 1
                    success_count += 1
        except Exception as e:
            print(f"处理年份{year}时出错: {str(e)}")
            error_count += 1
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\n重新生成完成")
    print(f"总处理: {total_count}")
    print(f"成功: {success_count}")
    print(f"失败: {error_count}")

if __name__ == "__main__":
    # 生成缺失年份的节气数据
    generate_missing_terms()
    
    # 重新生成测试用例中使用的年份的节气数据
    test_years = [1955, 1960, 1989, 1990, 1991, 2007, 2008, 2009, 2021, 2022, 2023, 2024]
    regenerate_terms_for_years(test_years)
