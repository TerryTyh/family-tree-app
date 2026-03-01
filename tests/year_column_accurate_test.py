#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
年柱精准测试脚本
验证各种边界场景下的年柱计算准确性
"""

import datetime
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')

from year_column import calculate_year_pillar

# 精准测试用例
accurate_test_cases = [
    # ========== 场景1：腊月立春（跨农历年） ==========
    # 验证：2017年立春在2月3日，腊月廿五出生仍属2016年
    {
        "name": "2017年腊月立春前（归属2016）",
        "birth_bt": datetime.datetime(2017, 1, 30, 12, 0, 0),
        "longitude": 120.19,  # 杭州精准经度
        "spring_start_bt": datetime.datetime(2017, 2, 3, 23, 34),  # 精准立春时间
        "expected": "丙申"  # 验证依据：出生早于立春，归属2016年
    },
    # 验证：2017年立春后出生，归属2017年
    {
        "name": "2017年立春后（归属2017）",
        "birth_bt": datetime.datetime(2017, 2, 4, 0, 0, 0),
        "longitude": 120.19,
        "spring_start_bt": datetime.datetime(2017, 2, 3, 23, 34),
        "expected": "丁酉"  # 验证依据：出生晚于立春，归属2017年
    },

    # ========== 场景2：立春当天跨时（分钟级精准） ==========
    # 验证：2008年立春19:03，19:00出生属2007年
    {
        "name": "2008年立春前（19:00）",
        "birth_bt": datetime.datetime(2008, 2, 4, 19, 0, 0),
        "longitude": 116.40,  # 北京精准经度
        "spring_start_bt": datetime.datetime(2008, 2, 4, 19, 3),
        "expected": "丁亥"  # 验证依据：早于立春3分钟，归属2007年
    },
    # 验证：2008年立春19:03，19:04出生属2008年
    {
        "name": "2008年立春后（19:04）",
        "birth_bt": datetime.datetime(2008, 2, 4, 19, 4, 0),
        "longitude": 116.40,
        "spring_start_bt": datetime.datetime(2008, 2, 4, 19, 3),
        "expected": "戊子"  # 验证依据：晚于立春1分钟，归属2008年
    },

    # ========== 场景3：极端立春时间（凌晨/深夜） ==========
    # 验证：1966年立春00:28，23:00出生属1965年
    {
        "name": "1966年立春前（凌晨）",
        "birth_bt": datetime.datetime(1966, 2, 3, 23, 0, 0),
        "longitude": 102.73,  # 昆明精准经度
        "spring_start_bt": datetime.datetime(1966, 2, 4, 0, 28),
        "expected": "乙巳"  # 验证依据：早于立春，归属1965年
    },
    # 验证：1966年立春00:28，01:00出生属1966年
    {
        "name": "1966年立春后（凌晨）",
        "birth_bt": datetime.datetime(1966, 2, 4, 1, 0, 0),
        "longitude": 102.73,
        "spring_start_bt": datetime.datetime(1966, 2, 4, 0, 28),
        "expected": "丙午"  # 验证依据：晚于立春，归属1966年
    },
    # 验证：1989年立春23:26，22:00出生属1988年
    {
        "name": "1989年立春前（深夜）",
        "birth_bt": datetime.datetime(1989, 2, 4, 22, 0, 0),
        "longitude": 119.65,  # 苏州精准经度
        "spring_start_bt": datetime.datetime(1989, 2, 4, 23, 26),
        "expected": "戊辰"  # 验证依据：早于立春，归属1988年
    },
    # 验证：1989年立春23:26，23:30出生属1989年
    {
        "name": "1989年立春后（深夜）",
        "birth_bt": datetime.datetime(1989, 2, 4, 23, 30, 0),
        "longitude": 119.65,
        "spring_start_bt": datetime.datetime(1989, 2, 4, 23, 26),
        "expected": "己巳"  # 验证依据：晚于立春，归属1989年
    },

    # ========== 场景4：经度边界值（含抚远/喀什） ==========
    # 验证：抚远（134.27°，最东端）2020年出生
    {
        "name": "2020年（抚远经度，最东端）",
        "birth_bt": datetime.datetime(2020, 3, 1, 10, 0, 0),
        "longitude": 134.27,  # 抚远精准经度（73~135.5°内）
        "spring_start_bt": datetime.datetime(2020, 2, 4, 17, 3),
        "expected": "庚子"  # 验证依据：立春后出生，归属2020年
    },
    # 验证：喀什（73.98°，最西端）1999年出生
    {
        "name": "1999年（喀什经度，最西端）",
        "birth_bt": datetime.datetime(1999, 6, 1, 12, 0, 0),
        "longitude": 73.98,  # 喀什精准经度（73~135.5°内）
        "spring_start_bt": datetime.datetime(1999, 2, 4, 14, 42),
        "expected": "己卯"  # 验证依据：立春后出生，归属1999年
    },

    # ========== 场景5：小年立春（2025年） ==========
    # 验证：2025年立春2月3日12:59，1月29日出生属2024年
    {
        "name": "2025年小年立春前（归属2024）",
        "birth_bt": datetime.datetime(2025, 1, 29, 10, 0, 0),
        "longitude": 118.01,  # 天津精准经度
        "spring_start_bt": datetime.datetime(2025, 2, 3, 12, 59),
        "expected": "甲辰"  # 验证依据：早于立春，归属2024年
    },
    # 验证：2025年立春后出生，归属2025年
    {
        "name": "2025年小年立春后（归属2025）",
        "birth_bt": datetime.datetime(2025, 2, 3, 13, 0, 0),
        "longitude": 118.01,
        "spring_start_bt": datetime.datetime(2025, 2, 3, 12, 59),
        "expected": "乙巳"  # 验证依据：晚于立春，归属2025年
    },

    # ========== 场景6：60甲子循环验证 ==========
    # 验证：1924（甲子）、2044（甲子）60年循环
    {
        "name": "1924年（甲子年，60甲子起点）",
        "birth_bt": datetime.datetime(1924, 3, 1, 8, 0, 0),
        "longitude": 114.05,  # 深圳精准经度
        "spring_start_bt": datetime.datetime(1924, 2, 5, 0, 12),
        "expected": "甲子"  # 验证依据：60甲子循环，1924为甲子
    },
    {
        "name": "2044年（甲子年，60年循环）",
        "birth_bt": datetime.datetime(2044, 3, 1, 15, 0, 0),
        "longitude": 106.55,  # 重庆精准经度
        "spring_start_bt": datetime.datetime(2044, 2, 4, 2, 10),
        "expected": "甲子"  # 验证依据：1924+60=2044，仍为甲子
    },

    # ========== 场景7：海外华人（新加坡，UTC+8） ==========
    {
        "name": "2018年（新加坡经度，UTC+8）",
        "birth_bt": datetime.datetime(2018, 4, 1, 12, 0, 0),
        "longitude": 103.82,  # 新加坡精准经度（73~135.5°内）
        "spring_start_bt": datetime.datetime(2018, 2, 4, 5, 28),
        "expected": "戊戌"  # 验证依据：立春后出生，归属2018年
    }
]

if __name__ == "__main__":
    print("开始执行年柱精准测试...")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for idx, case in enumerate(accurate_test_cases, 1):
        try:
            actual = calculate_year_pillar(case["birth_bt"], case["longitude"])
            status = "✅ 成功" if actual == case["expected"] else "❌ 失败"
            print(f"[{idx}] {case['name']} | 预期: {case['expected']} | 实际: {actual} | {status}")
            
            if actual == case["expected"]:
                passed += 1
            else:
                failed += 1
                print(f"  出生时间: {case['birth_bt'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  经度: {case['longitude']}°E")
                print(f"  立春时间: {case['spring_start_bt'].strftime('%Y-%m-%d %H:%M:%S')}")
                print()
        except Exception as e:
            print(f"[{idx}] {case['name']} | 执行错误: {str(e)}")
            failed += 1
            print()
    
    print("=" * 80)
    print(f"测试完成 | 成功: {passed} | 失败: {failed} | 总测试数: {len(accurate_test_cases)}")
    
    if failed == 0:
        print("🎉 所有测试用例均通过！年柱计算准确。")
    else:
        print("⚠️  部分测试用例失败，需要进一步优化。")
