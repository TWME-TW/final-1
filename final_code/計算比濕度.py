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