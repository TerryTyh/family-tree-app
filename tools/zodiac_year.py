# 批量测试脚本
import datetime
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')

from year_column import calculate_year_pillar

if __name__ == "__main__":
    # 定义测试用例列表
    test_cases = [
        {
            "name": "1950年（早于1984）",
            "birth_bt": datetime.datetime(1950, 3, 1, 10, 0, 0),
            "longitude": 116.40,
            "expected": "庚寅"
        },
        {
            "name": "1984年立春前",
            "birth_bt": datetime.datetime(1984, 2, 3, 12, 0, 0),
            "longitude": 116.40,
            "expected": "癸亥"
        },
        {
            "name": "1984年立春后",
            "birth_bt": datetime.datetime(1984, 2, 5, 10, 0, 0),
            "longitude": 116.40,
            "expected": "甲子"
        },
        {
            "name": "2000年立春前",
            "birth_bt": datetime.datetime(2000, 1, 20, 8, 0, 0),
            "longitude": 121.47,
            "expected": "己卯"
        },
        {
            "name": "2024年立春后",
            "birth_bt": datetime.datetime(2024, 2, 5, 10, 0, 0),
            "longitude": 104.06,
            "expected": "甲辰"
        },
        {
            "name": "1937年（民国）",
            "birth_bt": datetime.datetime(1937, 5, 1, 14, 0, 0),
            "longitude": 91.13,
            "expected": "丁丑"
        },
        {
            "name": "1900年（清末）",
            "birth_bt": datetime.datetime(1900, 6, 1, 9, 0, 0),
            "longitude": 120.00,
            "expected": "庚子"
        },
        # 修正后的测试用例8
        {
            "name": "2023年立春后",
            "birth_bt": datetime.datetime(2023, 2, 4, 11, 0, 0),  # 从10:00改成11:00
            "longitude": 113.23,
            "expected": "癸卯"
        },
        {
            "name": "2023年立春前",
            "birth_bt": datetime.datetime(2023, 2, 4, 9, 0, 0),
            "longitude": 113.23,
            "expected": "壬寅"
        }
    ]

    # 新增测试用例
    additional_cases = [
        # 10. 跨世纪腊月立春（2017年立春在腊月，出生在腊月立春后）
        {
            "name": "2017年腊月立春前",
            "birth_bt": datetime.datetime(2017, 1, 30, 12, 0, 0),  # 2017年立春在2017-02-03
            "longitude": 120.19,  # 杭州经度
            "expected": "丙申"
        },
        {
            "name": "2017年腊月立春后",
            "birth_bt": datetime.datetime(2017, 2, 4, 0, 0, 0),  # 调整到立春后（23:34之后）
            "longitude": 120.19,
            "expected": "丁酉"
        },
        # 11. 2008年立春当天跨时（北京经度）
        {
            "name": "2008年立春当天（前）",
            "birth_bt": datetime.datetime(2008, 2, 4, 19, 0, 0),  # 2008立春北京时间19:03
            "longitude": 116.40,  # 北京经度
            "expected": "丁亥"
        },
        {
            "name": "2008年立春当天（后）",
            "birth_bt": datetime.datetime(2008, 2, 4, 19, 4, 0),
            "longitude": 116.40,
            "expected": "戊子"
        },
        # 12. 1970年（庚戌年，早于1984，拉萨经度）
        {
            "name": "1970年（拉萨经度）",
            "birth_bt": datetime.datetime(1970, 5, 1, 10, 0, 0),
            "longitude": 91.13,  # 拉萨经度
            "expected": "庚戌"
        },
        # 13. 1924年（甲子年，60甲子循环验证）
        {
            "name": "1924年（甲子年）",
            "birth_bt": datetime.datetime(1924, 3, 1, 8, 0, 0),
            "longitude": 114.05,  # 深圳经度
            "expected": "甲子"
        },
        # 14. 2044年（下一个甲子年，验证60年循环）
        {
            "name": "2044年（甲子年）",
            "birth_bt": datetime.datetime(2044, 3, 1, 15, 0, 0),
            "longitude": 106.55,  # 重庆经度
            "expected": "甲子"
        },
        # 15. 1960年（庚子年，验证负数取模）
        {
            "name": "1960年（庚子年）",
            "birth_bt": datetime.datetime(1960, 4, 1, 9, 0, 0),
            "longitude": 121.47,  # 上海经度
            "expected": "庚子"
        },
        # 16. 2010年立春前（归属2009年）
        {
            "name": "2010年立春前（归属2009）",
            "birth_bt": datetime.datetime(2010, 2, 3, 10, 0, 0),  # 2010立春2月4日
            "longitude": 113.23,  # 广州经度
            "expected": "己丑"
        },
        # 17. 极端经度（最西端喀什，73°E）
        {
            "name": "1999年（喀什经度）",
            "birth_bt": datetime.datetime(1999, 6, 1, 12, 0, 0),
            "longitude": 73.98,  # 喀什经度（最西端）
            "expected": "己卯"
        },
        # 18. 极端经度（最东端抚远，135°E）
        {
            "name": "2020年（抚远经度）",
            "birth_bt": datetime.datetime(2020, 3, 1, 10, 0, 0),
            "longitude": 134.27,  # 抚远经度（最东端）
            "expected": "庚子"
        }
    ]

    # 合并测试用例
    test_cases.extend(additional_cases)

    # 追加到test_cases末尾的补充用例
    additional_special_cases = [
        # 20. 2025年小年立春（2025年立春在腊月廿六，出生在立春后）
        {
            "name": "2025年小年立春后",
            "birth_bt": datetime.datetime(2025, 2, 3, 13, 0, 0),  # 2025立春:2025-02-03 12:59
            "longitude": 118.01,  # 天津经度
            "expected": "乙巳"
        },
        # 21. 1995年闰八月出生（验证闰月不影响年柱）
        {
            "name": "1995年闰八月出生",
            "birth_bt": datetime.datetime(1995, 10, 1, 15, 0, 0),  # 1995闰八月
            "longitude": 108.33,  # 南宁经度
            "expected": "乙亥"
        },
        # 22. 1912年（民国元年，跨朝代）
        {
            "name": "1912年（民国元年）",
            "birth_bt": datetime.datetime(1912, 5, 1, 8, 0, 0),
            "longitude": 122.20,  # 宁波经度
            "expected": "壬子"
        },
        # 23. 1989年立春极晚（1989-02-04 23:26，验证深夜立春）
        {
            "name": "1989年立春前（深夜）",
            "birth_bt": datetime.datetime(1989, 2, 4, 22, 0, 0),
            "longitude": 119.65,  # 苏州经度
            "expected": "戊辰"
        },
        {
            "name": "1989年立春后（深夜）",
            "birth_bt": datetime.datetime(1989, 2, 5, 0, 0, 0),
            "longitude": 119.65,
            "expected": "己巳"
        },
        # 24. 1966年立春极早（1966-02-04 00:28，验证凌晨立春）
        {
            "name": "1966年立春前（凌晨）",
            "birth_bt": datetime.datetime(1966, 2, 3, 23, 0, 0),
            "longitude": 102.73,  # 昆明经度
            "expected": "乙巳"
        },
        {
            "name": "1966年立春后（凌晨）",
            "birth_bt": datetime.datetime(1966, 2, 4, 1, 0, 0),
            "longitude": 102.73,
            "expected": "丙午"
        },
        # 25. 海外华人（新加坡，经度103.82°，仍属UTC+8）
        {
            "name": "2018年（新加坡经度）",
            "birth_bt": datetime.datetime(2018, 4, 1, 12, 0, 0),
            "longitude": 103.82,  # 新加坡经度（属中国时区）
            "expected": "戊戌"
        },
        # 26. 1949年（建国元年）
        {
            "name": "1949年（建国元年）",
            "birth_bt": datetime.datetime(1949, 10, 1, 15, 0, 0),
            "longitude": 116.40,  # 北京经度
            "expected": "己丑"
        },
        # 27. 2030年（未来年份，验证公式兜底）
        {
            "name": "2030年（未来年份）",
            "birth_bt": datetime.datetime(2030, 6, 1, 9, 0, 0),
            "longitude": 112.55,  # 武汉经度
            "expected": "庚戌"
        },
        # 28. 1901年（辛丑年，验证1900后第一年）
        {
            "name": "1901年（辛丑年）",
            "birth_bt": datetime.datetime(1901, 3, 1, 10, 0, 0),
            "longitude": 109.78,  # 西安经度
            "expected": "辛丑"
        }
    ]

    # 合并所有用例
    test_cases += additional_special_cases

    # 执行测试
    for idx, case in enumerate(test_cases, 1):
        try:
            actual = calculate_year_pillar(case["birth_bt"], case["longitude"])
            status = "✅ 成功" if actual == case["expected"] else "❌ 失败"
            print(f"[{idx}] {case['name']} | 预期: {case['expected']} | 实际: {actual} | {status}")
        except Exception as e:
            print(f"[{idx}] {case['name']} | 执行错误: {str(e)}")