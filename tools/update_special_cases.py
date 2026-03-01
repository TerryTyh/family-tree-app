#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新特殊年份的节气时间到数据库
"""

import sqlite3
import datetime
import sys
import os
from datetime import datetime, timedelta

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')
from solar_time import calculate_true_solar_time

# 数据库文件路径
import os
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'solar_terms.db')

# 特殊年份的节气时间调整
special_cases = {
    (1960, "立春"): datetime(1960, 2, 5, 3, 23, 9),
    (1990, "立夏"): datetime(1990, 5, 6, 2, 38, 26),
    (2008, "冬至"): datetime(2008, 12, 21, 20, 7, 54),
    (2023, "立春"): datetime(2023, 2, 4, 10, 42),
    (2024, "立春"): datetime(2024, 2, 4, 16, 26),
    (1955, "芒种"): datetime(1955, 6, 6, 17, 38, 32)
}

# 经度列表（需要更新的经度）
longitudes = [120.0, 116.40, 120.19, 102.73]

def update_special_cases():
    """
    更新特殊年份的节气时间到数据库
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    updated_count = 0
    
    print("开始更新特殊年份的节气时间...")
    
    for (year, term_name), bt in special_cases.items():
        print(f"处理 {year}年{term_name}")
        
        for longitude in longitudes:
            try:
                # 计算真太阳时
                true_solar = calculate_true_solar_time(bt, longitude)
                
                # 更新数据库
                cursor.execute('''
                UPDATE solar_terms 
                SET bt_datetime = ?, true_solar_datetime = ?
                WHERE year = ? AND term_name = ? AND longitude = ?
                ''', (bt.isoformat(), true_solar.isoformat(), year, term_name, longitude))
                
                if cursor.rowcount > 0:
                    updated_count += 1
                    print(f"  更新了经度 {longitude} 的数据")
                else:
                    # 如果记录不存在，插入新记录
                    cursor.execute('''
                    INSERT OR REPLACE INTO solar_terms (year, term_name, bt_datetime, longitude, true_solar_datetime)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (year, term_name, bt.isoformat(), longitude, true_solar.isoformat()))
                    updated_count += 1
                    print(f"  插入了经度 {longitude} 的数据")
            except Exception as e:
                print(f"  处理经度 {longitude} 时出错: {str(e)}")
                continue
    
    conn.commit()
    conn.close()
    
    print(f"\n更新完成")
    print(f"共更新/插入 {updated_count} 条记录")

if __name__ == "__main__":
    update_special_cases()
