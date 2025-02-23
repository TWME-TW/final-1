# ---------------------------------------------
# 模組1：溫度與飽和水氣壓對照表 (可自行增加更細緻數據)
# ---------------------------------------------
TEMP_VAPOR_TABLE = [
    (-10, 2.60),    # -10°C ≈ 2.60 hPa
    (0,   6.11),    # 0°C   ≈ 6.11 hPa
    (5,   8.72),
    (10,  12.27),
    (15,  17.05),
    (20,  23.40),
    (25,  31.17),
    (30,  42.18),
    (35,  56.20),
    (40,  73.75),
    (50,  123.4),
    (60,  199.26),
    (70,  311.69),
    (80,  473.67),
    (90,  701.13),
    (100, 1013.25)
]

# ---------------------------------------------
# 模組2：依照表計算飽和水氣壓
# ---------------------------------------------

def interpolate_vapor_pressure(temp, table=TEMP_VAPOR_TABLE):
    """
    根據溫度 temp (°C)，利用線性內插法從對照表中取得飽和水氣壓 (hPa)。
    若 temp 超出表格範圍，則回傳最接近的邊界值。
    """
    # 邊界處理
    if temp <= table[0][0]:
        return table[0][1]
    if temp >= table[-1][0]:
        return table[-1][1]

    # 線性內插
    for i in range(len(table) - 1):
        t1, e1 = table[i]
        t2, e2 = table[i + 1]
        if t1 <= temp <= t2:
            return e1 + (e2 - e1) / (t2 - t1) * (temp - t1)
    # 一般情況不會到這裡
    return table[-1][1]
