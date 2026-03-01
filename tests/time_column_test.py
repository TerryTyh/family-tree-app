#!/usr/bin/env python3
from datetime import datetime
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.time_column import calculate_time_column

def test_calculate_time_column():
    """测试时柱计算函数（单独的测试文件，不污染业务代码）"""
    test_cases = [
        # (真太阳时, 日柱天干, 预期时柱, 描述)
        (datetime(1960, 2, 5, 3, 22, 59), '壬', '壬寅', '测试用例1：1960-02-05 03:22:59（寅时）'),
        (datetime(1960, 2, 5, 3, 23, 9), '壬', '壬寅', '测试用例2：1960-02-05 03:23:09（寅时）'),
        (datetime(1990, 5, 6, 2, 35, 25), '辛', '己丑', '测试用例3：1990-05-06 02:35:25（丑时）'),
        (datetime(1990, 5, 6, 2, 35, 26), '辛', '己丑', '测试用例4：1990-05-06 02:35:26（丑时）'),
        (datetime(2008, 12, 21, 20, 4, 53), '乙', '丙戌', '测试用例5：2008-12-21 20:04:53（戌时）'),
        (datetime(2008, 12, 21, 20, 4, 54), '乙', '丙戌', '测试用例6：2008-12-21 20:04:54（戌时）'),
        (datetime(1955, 6, 6, 0, 0, 0), '庚', '丙子', '测试用例7：1955-06-06 00:00:00（子时）'),
        (datetime(2023, 1, 1, 0, 0, 0), '癸', '壬子', '测试用例8：2023-01-01 00:00:00（子时）'),
        (datetime(2024, 2, 4, 16, 26, 0), '壬', '戊申', '测试用例9：2024-02-04 16:26:00（申时）'),
        (datetime(2024, 2, 4, 23, 59, 59), '壬', '庚子', '测试用例10：2024-02-04 23:59:59（子时）'),
        (datetime(2024, 2, 5, 0, 0, 0), '壬', '庚子', '测试用例11：2024-02-05 00:00:00（子时）'),
        (datetime(2024, 2, 5, 0, 59, 59), '壬', '庚子', '测试用例12：2024-02-05 00:59:59（子时）'),
        (datetime(2024, 2, 5, 1, 0, 0), '壬', '辛丑', '测试用例13：2024-02-05 01:00:00（丑时）'),
    ]
    
    print("开始执行时柱测试...")
    print("=" * 80)
    
    pass_count = 0
    total_count = len(test_cases)
    
    for idx, (time, day_gan, expected, desc) in enumerate(test_cases):
        try:
            result = calculate_time_column(time, day_gan)
            passed = result == expected
            
            if passed:
                pass_count += 1
                print(f"✅ 测试用例{idx+1}通过：{desc}")
            else:
                print(f"❌ 测试用例{idx+1}失败：{desc}")
                print(f"  预期: {expected}，实际: {result}")
        except Exception as e:
            print(f"❌ 测试用例{idx+1}异常：{desc}")
            print(f"  错误: {str(e)}")
        print()
    
    print("=" * 80)
    print(f"测试完成 | 成功: {pass_count}/{total_count} | 失败: {total_count - pass_count}")
    
    if pass_count == total_count:
        print("🎉 所有测试用例均通过！时柱计算准确。")
    else:
        print("⚠️  部分测试用例失败，需要优化代码。")

if __name__ == "__main__":
    test_calculate_time_column()
