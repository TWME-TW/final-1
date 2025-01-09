import numpy as np

# 模組1: 溫度及水氣壓對照表
TEMP_VAPOR_TABLE = [
    (-10, 2.60),  # -10°C ≈ 2.60 hPa
    (0, 6.11),    # 0°C ≈ 6.11 hPa
    (5, 8.72),
    (10, 12.27),
    (15, 17.05),
    (20, 23.40),
    (25, 31.17),
    (30, 42.18),
    (35, 56.20),
    (40, 73.75),
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

# 模組2: 計算蒸氣壓
def calculate_vapor_pressure(pressures, temperatures):
    """
    根據壓力和溫度計算對應的蒸氣壓。
    pressures: 壓力列表 (hPa)
    temperatures: 溫度列表 (°C)
    返回: 蒸氣壓列表 (e, hPa)
    """
    vapor_pressures = []
    for temp in temperatures:
        vapor_pressures.append(interpolate_vapor_pressure(temp))
    return vapor_pressures

# 模組3: 計算比濕度
def calculate_specific_humidity(vapor_pressures, pressures):
    """
    根據蒸氣壓和壓力計算比濕度 (H_s = 622 * e / p)。
    vapor_pressures: 蒸氣壓列表 (hPa)
    pressures: 壓力列表 (hPa)
    返回: 比濕度列表
    """
    specific_humidity = []
    for e, p in zip(vapor_pressures, pressures):
        specific_humidity.append(622 * e / p)
    return specific_humidity

# 模組4: 計算可降水量
def calculate_precipitable_water(p_differences, H_avg):
    """
    根據壓力差和平均比濕度計算可降水量。
    p_differences: 壓力差列表
    H_avg: 平均比濕度列表
    返回: 可降水量 (W_p)
    """
    W_p = 0
    for p_diff, H in zip(p_differences, H_avg):
        W_p += 0.01 * H * p_diff
    return W_p

# 主程式
def main():
    # Step 1: 輸入壓力和溫度數據
    print("請輸入壓力 p 和對應溫度 c (格式: p1,c1 p2,c2 ...)，以空格分隔:")
    input_data = input()
    data_points = input_data.split()
    
    pressures = []
    temperatures = []
    
    for point in data_points:
        p, c = map(float, point.split(","))
        pressures.append(p)
        temperatures.append(c)
    
    # 計算蒸氣壓
    vapor_pressures = calculate_vapor_pressure(pressures, temperatures)
    
    # 計算比濕度
    specific_humidity = calculate_specific_humidity(vapor_pressures, pressures)
    
    # 計算壓力差
    pressure_differences = [abs(pressures[i] - pressures[i + 1]) for i in range(len(pressures) - 1)]
    
    # 計算平均比濕度
    average_specific_humidity = [(specific_humidity[i] + specific_humidity[i + 1]) / 2 for i in range(len(specific_humidity) - 1)]
    
    # 計算可降水量
    precipitable_water = calculate_precipitable_water(pressure_differences, average_specific_humidity)
    
    # 顯示結果
    print("\n計算結果:")
    for i, (p, c, e, H) in enumerate(zip(pressures, temperatures, vapor_pressures, specific_humidity), start=1):
        print(f"點{i}: 壓力={p}hPa, 溫度={c}°C, 蒸氣壓={e:.2f}hPa, 比濕度={H:.2f}g/kg")
    
    for i, (p_diff, H_avg) in enumerate(zip(pressure_differences, average_specific_humidity), start=1):
        print(f"壓力差{i}={p_diff}hPa, 平均比濕度{i}={H_avg:.2f}g/kg")
    
    print(f"\n可降水量 W_p={precipitable_water:.2f} mm")

# 執行主程式
if __name__ == "__main__":
    main()