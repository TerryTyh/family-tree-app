#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中的节气数据年份
"""

import sqlite3

# 数据库文件路径
import os
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'solar_terms.db')

# 检查数据库中的年份
def check_db_years():
    """
    检查数据库中已有的节气数据年份
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取所有年份
    cursor.execute('SELECT DISTINCT year FROM solar_terms ORDER BY year')
    db_years = [year[0] for year in cursor.fetchall()]
    
    conn.close()
    
    return db_years

# 找出缺失的年份
def find_missing_years(start_year=1900, end_year=2100, db_years=None):
    """
    找出1900-2100年中缺失的年份
    """
    if db_years is None:
        db_years = check_db_years()
    
    all_years = list(range(start_year, end_year + 1))
    missing_years = [year for year in all_years if year not in db_years]
    
    return missing_years

if __name__ == "__main__":
    print("检查数据库中的节气数据年份...")
    
    # 获取数据库中的年份
    db_years = check_db_years()
    print(f"数据库中已存入{len(db_years)}个年份的节气数据")
    print(f"已存入的年份: {db_years}")
    
    # 找出缺失的年份
    missing_years = find_missing_years(1900, 2100, db_years)
    print(f"\n缺失的年份数量: {len(missing_years)}")
    print(f"缺失的年份: {missing_years}")
    
    # 检查最近几年的数据
    recent_years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
    print("\n最近几年的存储情况:")
    for year in recent_years:
        status = "✅" if year in db_years else "❌"
        print(f"{year}: {status}")
