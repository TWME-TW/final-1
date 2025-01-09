# 模組1: 溫度及水氣壓對照表
TEMP_VAPOR_TABLE = [
    (-10, 2.60),  # -10°C ≈ 2.60 hPa
    (0, 6.11),    # 0°C ≈ 6.11 hPa
    (5, 8.72),
    (10, 12.27),
    (15, 17.04),
    (20, 23.37),
    (25, 31.67),
    (30, 42.43),
    (35, 56.24),
    (40, 73.78),
    (50, 123.4),
    (60, 199.26),
    (70, 311.69),
    (80, 473.67),
    (90, 701.13),
    (100, 1013.25)
]

def interpolate_vapor_pressure(temp):
    """
    根據 TEMP_VAPOR_TABLE 使用線性內插法計算給定溫度的飽和水氣壓。
    temp: 溫度 (°C)
    返回: 飽和水氣壓 (hPa)
    """
    for i in range(len(TEMP_VAPOR_TABLE) - 1):
        t1, e1 = TEMP_VAPOR_TABLE[i]
        t2, e2 = TEMP_VAPOR_TABLE[i + 1]
        if t1 <= temp <= t2:
            # 線性內插公式: e = e1 + (temp - t1) * (e2 - e1) / (t2 - t1)
            return e1 + (temp - t1) * (e2 - e1) / (t2 - t1)
    if temp < TEMP_VAPOR_TABLE[0][0]:
        return TEMP_VAPOR_TABLE[0][1]  # 溫度低於範圍，返回最小值
    if temp > TEMP_VAPOR_TABLE[-1][0]:
        return TEMP_VAPOR_TABLE[-1][1]  # 溫度高於範圍，返回最大值
