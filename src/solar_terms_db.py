#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节气数据存储到数据库
"""

import sqlite3
import math
from datetime import datetime, timedelta
from solar_time import calculate_true_solar_time

# 十二节气名称（按顺序）
SOLAR_TERMS = [
    "小寒", "大寒", "立春", "雨水", "惊蛰", "春分",
    "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
    "小暑", "大暑", "立秋", "处暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]

# 数据库文件路径
import os
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'solar_terms.db')

# 从数据库获取节气基础信息
def get_term_info_from_db(term_name):
    """
    从数据库获取节气基础信息
    :param term_name: 节气名称
    :return: (default_month, default_day, solar_degree)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 只需查任意一年的该节气，即可获取default属性（因为所有年份的default值相同）
    cursor.execute('''
    SELECT default_month, default_day, solar_degree
    FROM solar_terms
    WHERE term_name = ?
    LIMIT 1
    ''', (term_name,))
    
    res = cursor.fetchone()
    conn.close()
    
    if not res:
        raise ValueError(f"未找到{term_name}的基础规则")
    return res  # 返回 (month, day, solar_degree)

# 计算指定年份和节气的北京时间
def calculate_solar_term_bt(year, term_index):
    """
    计算指定年份和节气的北京时间
    :param year: 年份
    :param term_index: 节气索引（0-23）
    :return: 节气北京时间（datetime对象）
    """
    # 节气名称
    term_name = SOLAR_TERMS[term_index]
    
    # 从数据库获取节气基础信息
    month, day, target_degree = get_term_info_from_db(term_name)
    
    # 核心参数：基于国际天文联合会(IAU)的节气计算模型
    t = (year - 2000) / 100.0  # 儒略世纪数
    
    # 1. 计算节气的太阳黄经对应的儒略日（TDT）
    # 基础项
    jd_base = 2451545.0 + 365.242198781 * (year - 2000)
    # 修正项（太阳黄经偏移）
    delta_t = (target_degree - 359.2422) / 360  # 修正到回归年
    jd_solar = jd_base + 365.2422 * delta_t
    
    # 2. 精细修正（消除章动、岁差影响）
    # 岁差修正
    precession = 0.000025862 * t
    # 章动修正
    nutation = 0.000308 * math.sin(math.radians(125.04 - 0.052954 * year))
    jd_final = jd_solar + precession + nutation
    
    # 3. 儒略日转换为UTC时间
    unix_days = jd_final - 2440587.5
    utc_time = datetime(1970, 1, 1) + timedelta(days=unix_days)
    
    # 4. 转换为北京时间（UTC+8）
    bt = utc_time + timedelta(hours=8)
    
    # 5. 调整到正确的月份和日期
    bt = datetime(year, month, day, bt.hour, bt.minute, bt.second)
    
    return bt

# 计算指定年份所有节气的北京时间
def calculate_year_solar_terms(year):
    """
    计算指定年份所有节气的北京时间
    :param year: 年份
    :return: {节气名称: 北京时间datetime}
    """
    solar_terms_bt = {}
    for i, term_name in enumerate(SOLAR_TERMS):
        bt = calculate_solar_term_bt(year, i)
        solar_terms_bt[term_name] = bt
    return solar_terms_bt

# 从数据库获取节气真太阳时
def get_solar_terms_from_db(year, longitude=120.0):
    """
    从数据库获取指定年份和经度的节气真太阳时
    :param year: 年份
    :param longitude: 经度
    :return: {节气名称: 真太阳时datetime}
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT term_name, true_solar_datetime FROM solar_terms
    WHERE year = ? AND longitude = ?
    ''', (year, longitude))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        raise ValueError(f"数据库中没有{year}年{longitude}经度的节气数据")
    
    solar_terms_true = {}
    for term_name, true_solar_str in results:
        true_solar = datetime.fromisoformat(true_solar_str)
        solar_terms_true[term_name] = true_solar
    
    return solar_terms_true

# 获取指定年份所有节气的真太阳时
def get_solar_terms_true_solar(year: int, longitude: float) -> dict:
    """
    获取指定年份所有节气的真太阳时
    :param year: 年份
    :param longitude: 出生地经度
    :return: {节气名称: 真太阳时datetime}
    """
    try:
        # 从数据库获取
        print(f"尝试从数据库获取{year}年{longitude}经度的节气数据...")
        result = get_solar_terms_from_db(year, longitude)
        print(f"数据库获取成功，共{len(result)}个节气")
        if "立春" in result:
            print(f"立春时间：{result['立春']}")
        return result
    except Exception as e:
        # 数据库获取失败，使用节气计算算法
        print(f"数据库获取失败：{str(e)}")
        solar_terms_bt = calculate_year_solar_terms(year)
        
        solar_terms_true = {}
        for term_name, term_bt in solar_terms_bt.items():
            term_true = calculate_true_solar_time(term_bt, longitude)
            solar_terms_true[term_name] = term_true
        
        print(f"使用计算算法，立春时间：{solar_terms_true.get('立春')}")
        return solar_terms_true
