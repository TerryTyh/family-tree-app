#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
月柱测试脚本
验证月柱计算的准确性
"""

import datetime
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')

from year_column import calculate_year_pillar
from month_column import calculate_month_pillar

# 月柱测试用例
test_cases = [
    # 测试用例1：1960-02-05 03:22:59，预期月柱是丁丑
    {
        "name": "1960-02-05 03:22:59（立春前）",
        "birth_bt": datetime.datetime(1960, 2, 5, 3, 22, 59),
        "longitude": 120.0,
        "expected_year_pillar": "己亥",
        "expected_month_pillar": "丁丑"
    },
    # 测试用例2：1960-02-05 03:23:09，预期月柱是戊寅
    {
        "name": "1960-02-05 03:23:09（立春后）",
        "birth_bt": datetime.datetime(1960, 2, 5, 3, 23, 9),
        "longitude": 120.0,
        "expected_year_pillar": "庚子",
        "expected_month_pillar": "戊寅"
    },
    # 测试用例3：2008-12-21 20:04:54，预期月柱是甲子
    {
        "name": "2008-12-21 20:04:54（冬至后）",
        "birth_bt": datetime.datetime(2008, 12, 21, 20, 4, 54),
        "longitude": 120.0,
        "expected_year_pillar": "戊子",
        "expected_month_pillar": "甲子"
    },
    # 测试用例4：2023-01-01 00:00:00，预期月柱是壬子
    {
        "name": "2023-01-01 00:00:00（小寒后）",
        "birth_bt": datetime.datetime(2023, 1, 1, 0, 0, 0),
        "longitude": 120.0,
        "expected_year_pillar": "壬寅",
        "expected_month_pillar": "壬子"
    },
    # 新测试用例1：1990-05-06 02:38:25（立夏前，辰月）
    {
        "name": "1990-05-06 02:38:25（立夏前，辰月）",
        "birth_bt": datetime.datetime(1990, 5, 6, 2, 38, 25),
        "longitude": 116.40,
        "expected_year_pillar": "庚午",
        "expected_month_pillar": "庚辰"
    },
    # 新测试用例2：2008-12-21 20:07:55（冬至后，子月）
    {
        "name": "2008-12-21 20:07:55（冬至后，子月）",
        "birth_bt": datetime.datetime(2008, 12, 21, 20, 7, 55),
        "longitude": 120.19,
        "expected_year_pillar": "戊子",
        "expected_month_pillar": "甲子"
    },
    # 新测试用例3：1955-06-06 17:38:33（芒种后，午月）
    {
        "name": "1955-06-06 17:38:33（芒种后，午月）",
        "birth_bt": datetime.datetime(1955, 6, 6, 17, 38, 33),
        "longitude": 102.73,
        "expected_year_pillar": "乙未",
        "expected_month_pillar": "壬午"
    },
]

if __name__ == "__main__":
    print("开始执行月柱测试...")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for idx, case in enumerate(test_cases, 1):
        try:
            # 计算年柱
            year_pillar = calculate_year_pillar(case["birth_bt"], case["longitude"])
            # 计算月柱
            actual_month_pillar = calculate_month_pillar(case["birth_bt"], case["longitude"], year_pillar)
            
            # 验证年柱和月柱
            year_status = "✅ 成功" if year_pillar == case["expected_year_pillar"] else "❌ 失败"
            month_status = "✅ 成功" if actual_month_pillar == case["expected_month_pillar"] else "❌ 失败"
            
            print(f"[{idx}] {case['name']}")
            print(f"  年柱：预期 {case['expected_year_pillar']}，实际 {year_pillar} | {year_status}")
            print(f"  月柱：预期 {case['expected_month_pillar']}，实际 {actual_month_pillar} | {month_status}")
            
            if year_pillar == case["expected_year_pillar"] and actual_month_pillar == case["expected_month_pillar"]:
                passed += 1
            else:
                failed += 1
                print()
        except Exception as e:
            print(f"[{idx}] {case['name']} | 执行错误: {str(e)}")
            failed += 1
            print()
    
    print("=" * 80)
    print(f"测试完成 | 成功: {passed} | 失败: {failed} | 总测试数: {len(test_cases)}")
    
    if failed == 0:
        print("🎉 所有测试用例均通过！月柱计算准确。")
    else:
        print("⚠️  部分测试用例失败，需要进一步优化。")
