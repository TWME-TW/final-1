from 計算飽和水氣壓 import interpolate_vapor_pressure

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