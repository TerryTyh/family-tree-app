#!/usr/bin/env python3
from datetime import datetime, timedelta

# 查找正确的基准日期
tian_gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
di_zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 已知的日期和对应的日柱
known_dates = [
    ("2024-05-20", "己巳"),
    ("2023-12-31", "癸卯"),  # 2024-01-01的前一天
    ("1990-01-01", "甲子"),
]

# 尝试不同的基准日期
for base_year in range(1900, 2000, 10):
    base_date = datetime(base_year, 1, 1)
    print(f"\n尝试基准日期: {base_date}")
    
    for date_str, expected in known_dates:
        test_date = datetime.strptime(date_str, "%Y-%m-%d")
        delta_days = (test_date - base_date).days
        
        # 尝试不同的偏移量
        for offset in range(60):  # 60甲子循环
            gan_index = (delta_days + offset) % 10
            zhi_index = (delta_days + offset) % 12
            
            day_gan = tian_gan[gan_index]
            day_zhi = di_zhi[zhi_index]
            result = day_gan + day_zhi
            
            if result == expected:
                print(f"  日期: {date_str}, 预期: {expected}, 计算: {result}, 偏移: {offset}")
                break
