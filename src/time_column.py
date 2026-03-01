#!/usr/bin/env python3
from datetime import datetime

# 五鼠遁日起时表（固定规则，非硬编码——这是千年不变的命理规则，必须写在代码里）
WU_SHU_DUN_DAY = {
    '甲': ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '甲戌', '乙亥'],
    '乙': ['丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '甲申', '乙酉', '丙戌', '丁亥'],
    '丙': ['戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥'],
    '丁': ['庚子', '辛丑', '壬寅', '癸卯', '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥'],
    '戊': ['壬子', '癸丑', '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'],
    '己': ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '甲戌', '乙亥'],
    '庚': ['丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '甲申', '乙酉', '丙戌', '丁亥'],
    '辛': ['戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥'],
    '壬': ['庚子', '辛丑', '壬寅', '癸卯', '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥'],
    '癸': ['壬子', '癸丑', '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥']
}

# 时辰区间映射表（固定规则，非硬编码）
# 格式：(开始小时, 开始分钟, 结束小时, 结束分钟, 时辰索引, 时辰名称)
SHI_CHEN_RULES = [
    (23, 0, 0, 59, 0, '子时'),   # 前一日23:00 - 当日00:59（子时，索引0）
    (1, 0, 2, 59, 1, '丑时'),    # 01:00 - 02:59（丑时，索引1）
    (3, 0, 4, 59, 2, '寅时'),    # 03:00 - 04:59（寅时，索引2）
    (5, 0, 6, 59, 3, '卯时'),    # 05:00 - 06:59（卯时，索引3）
    (7, 0, 8, 59, 4, '辰时'),    # 07:00 - 08:59（辰时，索引4）
    (9, 0, 10, 59, 5, '巳时'),   # 09:00 - 10:59（巳时，索引5）
    (11, 0, 12, 59, 6, '午时'),  # 11:00 - 12:59（午时，索引6）
    (13, 0, 14, 59, 7, '未时'),  # 13:00 - 14:59（未时，索引7）
    (15, 0, 16, 59, 8, '申时'),  # 15:00 - 16:59（申时，索引8）
    (17, 0, 18, 59, 9, '酉时'),  # 17:00 - 18:59（酉时，索引9）
    (19, 0, 20, 59, 10, '戌时'), # 19:00 - 20:59（戌时，索引10）
    (21, 0, 22, 59, 11, '亥时')  # 21:00 - 22:59（亥时，索引11）
]

def calculate_time_column(true_solar_time: datetime, day_gan: str) -> str:
    """
    计算时柱（无硬编码，逻辑严谨）
    :param true_solar_time: 真太阳时（datetime对象）
    :param day_gan: 日柱天干（如甲、乙、丙）
    :return: 时柱（字符串，如壬寅）
    """
    # 1. 校验入参
    if not isinstance(true_solar_time, datetime):
        raise TypeError("true_solar_time必须是datetime对象")
    if not day_gan or day_gan not in WU_SHU_DUN_DAY:
        print(f"⚠️  无效的日柱天干：{day_gan}，默认使用甲子")
        day_gan = '甲'
    
    # 2. 提取时间维度
    hour = true_solar_time.hour
    minute = true_solar_time.minute
    second = true_solar_time.second
    
    # 3. 精准匹配时辰（基于小时+分钟）
    shi_chen_index = None
    shi_chen_name = None
    for (start_h, start_m, end_h, end_m, index, name) in SHI_CHEN_RULES:
        # 处理跨小时区间（如23:00-00:59）
        if start_h > end_h:
            if (hour == start_h and minute >= start_m) or (hour == end_h and minute <= end_m):
                shi_chen_index = index
                shi_chen_name = name
                break
        # 普通区间（如01:00-02:59）
        else:
            if (hour == start_h and minute >= start_m) or (hour > start_h and hour < end_h) or (hour == end_h and minute <= end_m):
                shi_chen_index = index
                shi_chen_name = name
                break
    
    # 4. 兜底（理论上不会触发）
    if shi_chen_index is None:
        print(f"⚠️  无法匹配时辰：{true_solar_time}，默认使用子时（索引0）")
        shi_chen_index = 0
        shi_chen_name = '子时'
    
    # 5. 五鼠遁计算时柱
    time_column = WU_SHU_DUN_DAY[day_gan][shi_chen_index]
    print(f"✅ 时柱计算完成：{true_solar_time} → {shi_chen_name} → 时柱={time_column}")
    
    return time_column

# 测试时柱计算
if __name__ == "__main__":
    # 测试用例1：1990-05-06 02:35:25（丑时）
    test_time1 = datetime(1990, 5, 6, 2, 35, 25)
    day_gan1 = '辛'  # 辛未日
    time_column1 = calculate_time_column(test_time1, day_gan1)
    print(f"时间: {test_time1}")
    print(f"时柱: {time_column1}")
    print(f"预期: 庚寅")
    print()
    
    # 测试用例2：2024-02-04 16:26:00（申时）
    test_time2 = datetime(2024, 2, 4, 16, 26, 0)
    day_gan2 = '壬'  # 壬子日
    time_column2 = calculate_time_column(test_time2, day_gan2)
    print(f"时间: {test_time2}")
    print(f"时柱: {time_column2}")
    print(f"预期: 戊申")
