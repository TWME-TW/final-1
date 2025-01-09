#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from 封裝過後的資料格式 import PWInput, PWOutput
from 比濕度 import calc_mixing_ratio
from 查表獲得最近的水氣壓 import interpolate_vapor_pressure
from 內插法 import interpolate_point
from 梯形積分 import integrate_Hs_over_p
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