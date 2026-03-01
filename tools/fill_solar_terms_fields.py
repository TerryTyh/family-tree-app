#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量填充solar_terms表的基础字段
"""

import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'solar_terms.db')

def fill_solar_terms_base_fields():
    """
    批量填充default_month/default_day/solar_degree字段
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # term_info + SOLAR_TERMS_DEGREES的映射关系（仅这一次硬编码，之后不再改）
    base_mapping = {
        "小寒": (1, 6, 285),
        "大寒": (1, 20, 300),
        "立春": (2, 4, 315),
        "雨水": (2, 19, 330),
        "惊蛰": (3, 6, 345),
        "春分": (3, 21, 0),
        "清明": (4, 5, 15),
        "谷雨": (4, 20, 30),
        "立夏": (5, 6, 45),
        "小满": (5, 21, 60),
        "芒种": (6, 6, 75),
        "夏至": (6, 21, 90),
        "小暑": (7, 7, 105),
        "大暑": (7, 23, 120),
        "立秋": (8, 8, 135),
        "处暑": (8, 23, 150),
        "白露": (9, 8, 165),
        "秋分": (9, 23, 180),
        "寒露": (10, 8, 195),
        "霜降": (10, 23, 210),
        "立冬": (11, 7, 225),
        "小雪": (11, 22, 240),
        "大雪": (12, 7, 255),
        "冬至": (12, 22, 270)
    }
    
    # 批量更新
    for term_name, (month, day, degree) in base_mapping.items():
        cursor.execute('''
        UPDATE solar_terms
        SET default_month = ?, default_day = ?, solar_degree = ?
        WHERE term_name = ?
        ''', (month, day, degree, term_name))
        print(f"更新了{term_name}的基础字段")
    
    conn.commit()
    conn.close()
    print("基础字段填充完成")

if __name__ == "__main__":
    fill_solar_terms_base_fields()
