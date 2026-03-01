# zodiac_year.py（年柱计算文件）
import datetime
from solar_time import calculate_true_solar_time, get_spring_start_bt  # 导入真太阳时函数和立春时间计算函数

# 六十甲子表（固定顺序，无需修改）
ZODIAC_CYCLE = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未",
    "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯",
    "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥",
    "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未",
    "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
    "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥",
    "壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未",
    "庚申", "辛酉", "壬戌", "癸亥"
]

def get_spring_start_true_solar_time(year: int, longitude: float) -> datetime.datetime:
    """
    计算指定年份「立春」的真太阳时（简化版，精准版需查万年历/天文算法）
    :param year: 公历年
    :param longitude: 出生地经度
    :return: 立春的真太阳时（datetime）
    """
    # 注：实际立春时间需查精准天文数据，此处为通用简化值（可替换为精准万年历数据）
    # 示例：1900-2050年立春大致在2月3-5日，取常见值2月4日12:00北京时间为基准
    spring_start_bt = datetime.datetime(year, 2, 4, 12, 0, 0)
    # 转换为出生地真太阳时
    spring_start_true = calculate_true_solar_time(spring_start_bt, longitude)
    return spring_start_true

def calculate_year_pillar(birth_datetime_bt: datetime.datetime, longitude: float) -> str:
    """
    计算年柱（适配所有年份，结合真太阳时判断立春）
    :param birth_datetime_bt: 出生北京时间（datetime，含时分秒）
    :param longitude: 出生地东经度数（73°~135°）
    :return: 年柱（如甲子、乙丑）
    """
    # 1. 计算出生的真太阳时
    birth_true_solar = calculate_true_solar_time(birth_datetime_bt, longitude)
    
    # 2. 确定出生年份（先按公历，后续用立春修正）
    birth_year = birth_true_solar.year
    
    # 3. 计算当年立春的真太阳时（优化后）
    spring_start_bt = get_spring_start_bt(birth_year)
    # 校验：确保立春时间在合理范围（2月3-5日）
    if not (spring_start_bt.month == 2 and 3 <= spring_start_bt.day <=5):
        spring_start_bt = datetime.datetime(birth_year, 2, 4, 12, 0)  # 兜底值
    spring_start_true = calculate_true_solar_time(spring_start_bt, longitude)
    
    # 调试信息：打印立春时间和出生时间
    # if birth_year == 2023:
    #     print(f"调试信息 - 2023年:")
    #     print(f"出生北京时间: {birth_datetime_bt.strftime('%Y-%m-%d %H:%M:%S')}")
    #     print(f"出生真太阳时: {birth_true_solar.strftime('%Y-%m-%d %H:%M:%S')}")
    #     print(f"立春北京时间: {spring_start_bt.strftime('%Y-%m-%d %H:%M:%S')}")
    #     print(f"立春真太阳时: {spring_start_true.strftime('%Y-%m-%d %H:%M:%S')}")
    #     print(f"出生真太阳时 < 立春真太阳时: {birth_true_solar < spring_start_true}")
    
    # 4. 判断是否跨立春：若出生真太阳时在立春前，年柱归属上一年
    if birth_true_solar < spring_start_true:
        target_year = birth_year - 1
    else:
        target_year = birth_year
    
    # 5. 计算年柱索引（适配所有年份，无论早于/晚于1984）
    base_year = 1984  # 仍用1984（甲子年）为基准，取模自动适配所有年份
    year_diff = target_year - base_year
    pillar_index = year_diff % 60  # 取模60实现甲子循环（负数取模也会自动转正）
    
    return ZODIAC_CYCLE[pillar_index]

# 测试用例（覆盖早于1984的年份）
if __name__ == "__main__":
    # 测试1：1950年出生（早于1984），北京经度116.40
    birth_bt1 = datetime.datetime(1950, 3, 1, 10, 0, 0)
    year_pillar1 = calculate_year_pillar(birth_bt1, 116.40)
    print(f"1950年出生年柱：{year_pillar1}")  # 应输出"庚寅"
    
    # 测试2：1984年立春前出生（归属1983年）
    birth_bt2 = datetime.datetime(1984, 2, 3, 12, 0, 0)  # 立春前
    year_pillar2 = calculate_year_pillar(birth_bt2, 116.40)
    print(f"1984年立春前出生年柱：{year_pillar2}")  # 应输出"癸亥"（1983年）