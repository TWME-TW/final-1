#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pw_module.py

本檔案提供可降水量 (W_p) 計算的模組：
1. 資料結構：
   - PWInput: 儲存 (p, c) 清單 + h1, h2 (壓力範圍)
   - PWOutput: 儲存「每筆資料對應的水氣壓、比濕度」及「積分分段資訊」與「最終可降水量」等

2. 功能函式：
   - interpolate_vapor_pressure: 根據溫度內插飽和水氣壓
   - calc_mixing_ratio: 計算比濕度
   - integrate_Hs_over_p: 對 [h1, h2] 區間的 (p, H_s) 做梯形積分
   - compute_precipitable_water: 將上述步驟整合，產生 PWOutput
"""

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

class PWInput:
    """
    封裝『使用者輸入的原始資料』
    - data_points: List[ (p, c) ]，其中 p=壓力(hPa)，c=溫度(°C)
    - h1, h2: 欲計算可降水量的壓力上下邊界 (hPa)
    """
    def __init__(self, data_points=None, h1=None, h2=None):
        self.data_points = data_points if data_points else []
        self.h1 = h1
        self.h2 = h2

class PWOutput:
    """
    封裝『計算後要輸出的結果』
    - data_details: List[ (p, c, e, H_s) ]，每筆輸入對應的水氣壓/比濕度
    - segment_details: 梯形積分的各分段詳細資訊 (供輸出用)
    - total_integral: 在 [h1, h2] 間積分後的總面積 (H_s × Δp)
    - W_p: 0.01 * total_integral -> 最終可降水量(mm)
    """
    def __init__(self, data_details=None, segment_details=None, total_integral=0.0, W_p=0.0):
        self.data_details = data_details if data_details else []
        self.segment_details = segment_details if segment_details else []
        self.total_integral = total_integral
        self.W_p = W_p


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

def calc_mixing_ratio(e, p):
    """
    計算比濕度 H_s = 622 * e / p
    e, p (hPa)
    回傳值單位 ~ g/kg
    """
    return 622.0 * e / p

def interpolate_point(p_target, p1, p2, H_s1, H_s2):
    """
    在 p1, p2 間，針對 p_target 做 H_s 的線性內插。
    """
    return H_s1 + (H_s2 - H_s1) * ((p_target - p1) / (p2 - p1))

def integrate_Hs_over_p(data_points, h1, h2):
    """
    利用梯形公式，對在 [h1, h2] 區間的 (p, H_s) 做數值積分。
    data_points: 內部元素為 (p, H_s)，p 單位hPa, H_s 單位g/kg

    回傳:
      total_integral (float): ∫(H_s dP)
      segment_detail (list of dict): 每分段的詳細資訊
    """
    # 確保 h1, h2 誰大都可
    p_upper = max(h1, h2)
    p_lower = min(h1, h2)

    # 依 p 遞減排序
    data_sorted = sorted(data_points, key=lambda x: x[0], reverse=True)

    clipped = []
    for i in range(len(data_sorted) - 1):
        p_a, hs_a = data_sorted[i]
        p_b, hs_b = data_sorted[i+1]

        hi_local = max(p_a, p_b)
        lo_local = min(p_a, p_b)

        if hi_local < p_lower or lo_local > p_upper:
            # 無交集
            continue

        seg_upper = min(hi_local, p_upper)
        seg_lower = max(lo_local, p_lower)

        def get_Hs_at(p_target):
            # 若正好 == p_a or p_b，使用現有值；否則線性內插
            if abs(p_target - p_a) < 1e-9:
                return hs_a
            elif abs(p_target - p_b) < 1e-9:
                return hs_b
            else:
                return interpolate_point(p_target, p_a, p_b, hs_a, hs_b)

        hs_u = get_Hs_at(seg_upper)
        hs_l = get_Hs_at(seg_lower)

        clipped.append((seg_upper, hs_u))
        clipped.append((seg_lower, hs_l))

    # 去重
    clipped = list(set(clipped))
    # 依 p 遞減
    clipped_sorted = sorted(clipped, key=lambda x: x[0], reverse=True)

    total_integral = 0.0
    segment_detail = []
    for i in range(len(clipped_sorted) - 1):
        p1, hs1 = clipped_sorted[i]
        p2, hs2 = clipped_sorted[i+1]
        dp = abs(p1 - p2)
        mean_hs = (hs1 + hs2) / 2.0
        area = mean_hs * dp
        total_integral += area
        segment_detail.append({
            "p1": p1,
            "p2": p2,
            "H_s1": hs1,
            "H_s2": hs2,
            "mean_H_s": mean_hs,
            "Δp": dp,
            "area": area
        })

    return total_integral, segment_detail

def compute_precipitable_water(input_data: PWInput) -> PWOutput:
    """
    核心函式：綜合應用內插水氣壓、計算比濕度、在 [h1, h2] 間做梯形積分，最後算出W_p。
    回傳封裝好的 PWOutput。
    """
    # 1. 先把 (p, c) -> (p, e, H_s)
    data_details = []
    for (p_i, c_i) in input_data.data_points:
        e_i = interpolate_vapor_pressure(c_i)
        hs_i = calc_mixing_ratio(e_i, p_i)
        data_details.append((p_i, c_i, e_i, hs_i))

    # 2. 用 (p, H_s) 做梯形積分
    data_for_integration = [(p, hs) for (p, c, e, hs) in data_details]
    total_integral, seg_detail = integrate_Hs_over_p(data_for_integration, input_data.h1, input_data.h2)

    # 3. W_p = 0.01 * total_integral
    W_p = 0.01 * total_integral

    # 4. 封裝結果
    output_data = PWOutput(
        data_details=data_details,
        segment_details=seg_detail,
        total_integral=total_integral,
        W_p=W_p
    )
    return output_data