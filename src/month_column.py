#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
月柱计算模块
实现月柱地支映射、五虎遁年起月等功能
"""

from datetime import datetime
from solar_time import calculate_true_solar_time
from solar_terms_db import get_solar_terms_true_solar

# 月柱地支 → 对应节气区间（按顺序）
MONTH_ZHI_MAP = [
    ("丑", "小寒", "立春"),
    ("寅", "立春", "惊蛰"),
    ("卯", "惊蛰", "清明"),
    ("辰", "清明", "立夏"),
    ("巳", "立夏", "芒种"),
    ("午", "芒种", "小暑"),
    ("未", "小暑", "立秋"),
    ("申", "立秋", "白露"),
    ("酉", "白露", "寒露"),
    ("戌", "寒露", "立冬"),
    ("亥", "立冬", "大雪"),
    ("子", "大雪", "小寒"),
]

# 五虎遁年起月表：年干 → 寅月天干
FIVE_TIGERS_MAP = {
    "甲": "丙",
    "己": "丙",
    "乙": "戊",
    "庚": "戊",
    "丙": "庚",
    "辛": "庚",
    "丁": "壬",
    "壬": "壬",
    "戊": "甲",
    "癸": "甲",
}

# 天干顺序（用于顺推）
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

def get_month_zhi(birth_true_solar: datetime, solar_terms_true: dict) -> str:
    """
    根据出生真太阳时和节气真太阳时，确定月柱地支
    :param birth_true_solar: 出生真太阳时
    :param solar_terms_true: 合并了跨年份节气的数据字典
    :return: 月柱地支（如寅、卯）
    """
    # 1. 统一时间精度（去除微秒）
    birth_true_solar = birth_true_solar.replace(microsecond=0)
    
    # 2. 调试信息打印（完整且清晰）
    print(f"\n=== 月柱地支计算调试信息 ===")
    print(f"出生真太阳时：{birth_true_solar}")
    print(f"可用节气数据（仅展示关键节气）：")
    key_terms = ["大雪", "小寒", "立春", "惊蛰", "清明", "立夏", "芒种", "小暑", "立秋", "白露", "寒露", "立冬", "小雪",
                 "大雪_prev", "小寒_next", "立春_next", "立春_prev"]
    for term in key_terms:
        if term in solar_terms_true:
            print(f"  {term}: {solar_terms_true[term].replace(microsecond=0)}")
    
    # 3. 核心逻辑：按「子月→丑月→其他月份」的顺序匹配（解决逻辑顺序错误）
    for zhi, start_term, end_term in MONTH_ZHI_MAP:
        # 3.1 获取起始/结束节气的真太阳时（优先当前，再跨年度）
        start_time = None
        end_time = None
        
        # 处理起始节气（支持跨年度）
        if start_term in solar_terms_true:
            start_time = solar_terms_true[start_term]
        elif f"{start_term}_prev" in solar_terms_true:
            start_time = solar_terms_true[f"{start_term}_prev"]
        elif f"{start_term}_next" in solar_terms_true:
            start_time = solar_terms_true[f"{start_term}_next"]
        
        # 处理结束节气（支持跨年度）
        if end_term in solar_terms_true:
            end_time = solar_terms_true[end_term]
        elif f"{end_term}_prev" in solar_terms_true:
            end_time = solar_terms_true[f"{end_term}_prev"]
        elif f"{end_term}_next" in solar_terms_true:
            end_time = solar_terms_true[f"{end_term}_next"]
        
        # 3.2 跳过无数据的节气区间
        if not start_time or not end_time:
            continue
        
        # 3.3 统一精度后对比
        start_time = start_time.replace(microsecond=0)
        end_time = end_time.replace(microsecond=0)
        
        # 3.4 处理跨年度区间（核心！）
        is_cross_year = start_time.year < end_time.year
        match = False
        
        if is_cross_year:
            # 场景1：跨年度区间（如2023年大雪→2024年小寒）
            if (birth_true_solar.year == start_time.year and birth_true_solar >= start_time) or \
               (birth_true_solar.year == end_time.year and birth_true_solar < end_time):
                match = True
        else:
            # 场景2：同年度区间（如2023年立春→2023年惊蛰）
            if start_time <= birth_true_solar < end_time:
                match = True
        
        # 3.5 匹配成功则返回地支
        if match:
            print(f"✅ 匹配区间：{start_term}({start_time}) → {end_term}({end_time}) → 地支={zhi}")
            return zhi
    
    # 4. 兜底逻辑（仅作为最后保障，优先基于节气而非自然月）
    print(f"⚠️  未匹配任何节气区间，使用自然月兜底")
    month_to_zhi = {
        1: "丑", 2: "寅", 3: "卯", 4: "辰", 5: "巳", 6: "午",
        7: "未", 8: "申", 9: "酉", 10: "戌", 11: "亥", 12: "子"
    }
    default_zhi = month_to_zhi.get(birth_true_solar.month, "寅")
    print(f"📌 兜底返回：{default_zhi}")
    return default_zhi

def get_month_tian_gan(year_tian_gan: str, month_zhi: str) -> str:
    """
    根据年柱天干和月柱地支，用五虎遁年起月法确定月柱天干
    :param year_tian_gan: 年柱天干（如甲、乙）
    :param month_zhi: 月柱地支（如寅、卯）
    :return: 月柱天干（如丙、丁）
    """
    # 1. 找到寅月的天干
    yin_tian_gan = FIVE_TIGERS_MAP[year_tian_gan]
    
    # 2. 确定寅月在TIAN_GAN中的索引
    yin_index = TIAN_GAN.index(yin_tian_gan)
    
    # 3. 确定当前地支在MONTH_ZHI_MAP中的索引（从寅月开始算0）
    zhi_list = [zhi for zhi, _, _ in MONTH_ZHI_MAP]
    # 调整顺序：从寅月开始，到丑月结束
    adjusted_zhi_list = zhi_list[1:] + zhi_list[:1]  # [寅,卯,...,丑]
    month_zhi_index = adjusted_zhi_list.index(month_zhi)
    
    # 4. 顺推天干
    tian_gan_index = (yin_index + month_zhi_index) % 10
    return TIAN_GAN[tian_gan_index]

def get_cross_year_solar_terms(birth_year, longitude):
    """
    获取跨年份的节气数据，用于处理跨年的节气区间
    :param birth_year: 出生年份
    :param longitude: 出生地经度
    :return: 合并了跨年份节气的数据字典
    """
    # 获取当年、上一年、下一年的节气
    terms_curr = get_solar_terms_true_solar(birth_year, longitude)
    
    # 尝试获取上一年的节气数据
    try:
        terms_prev = get_solar_terms_true_solar(birth_year - 1, longitude)
    except ValueError:
        terms_prev = {}
    
    # 尝试获取下一年的节气数据
    try:
        terms_next = get_solar_terms_true_solar(birth_year + 1, longitude)
    except ValueError:
        terms_next = {}
    
    # 合并所有节气数据
    cross_terms = {}
    
    # 先添加当年的所有节气
    cross_terms.update(terms_curr)
    
    # 处理跨年节气
    # 上一年的大雪、小寒
    if "大雪" in terms_prev:
        cross_terms["大雪_prev"] = terms_prev["大雪"]
    if "小寒" in terms_prev:
        cross_terms["小寒_prev"] = terms_prev["小寒"]
    # 下一年的小寒、立春
    if "小寒" in terms_next:
        cross_terms["小寒_next"] = terms_next["小寒"]
    if "立春" in terms_next:
        cross_terms["立春_next"] = terms_next["立春"]
    # 当年的所有节气
    for term_name in ["立春", "惊蛰", "清明", "立夏", "芒种", "小暑", "立秋", "白露", "寒露", "立冬", "小雪", "大雪"]:
        if term_name in terms_curr:
            cross_terms[term_name] = terms_curr[term_name]
    
    # 去除所有节气时间的微秒，确保时间精度一致
    for term_name, term_time in cross_terms.items():
        if hasattr(term_time, 'replace'):
            cross_terms[term_name] = term_time.replace(microsecond=0)
    
    return cross_terms

def calculate_month_pillar(
    birth_datetime_bt: datetime,
    longitude: float,
    year_pillar: str
) -> str:
    """
    完整计算月柱
    :param birth_datetime_bt: 出生北京时间
    :param longitude: 出生地经度
    :param year_pillar: 年柱（如甲子、乙丑）
    :return: 月柱（如丙寅、丁卯）
    """
    # 1. 计算出生真太阳时
    birth_true_solar = calculate_true_solar_time(birth_datetime_bt, longitude)
    # 去除微秒，确保时间精度一致
    birth_true_solar = birth_true_solar.replace(microsecond=0)
    
    # 2. 确定出生年份（使用公历年）
    birth_year = birth_true_solar.year
    
    # 获取跨年份的节气数据，用于处理跨年的节气区间
    solar_terms_true = get_cross_year_solar_terms(birth_year, longitude)
    
    # 3. 确定月柱地支
    month_zhi = get_month_zhi(birth_true_solar, solar_terms_true)
    
    # 4. 确定月柱天干
    year_tian_gan = year_pillar[0]
    month_tian_gan = get_month_tian_gan(year_tian_gan, month_zhi)
    
    # 5. 组合月柱
    month_pillar = month_tian_gan + month_zhi
    
    return month_pillar
