#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main.py

此檔案作為「程式進入口」，示範如何使用 pw_module.py 提供的模組化功能。
1. 讀取使用者輸入 (p, c) 與 h1, h2，建構 PWInput 物件
2. 呼叫 compute_precipitable_water(PWInput) 得到 PWOutput
3. 最後印出結果 (包括水氣壓、比濕度、積分分段與 W_p 等)

說明：
    - 同目錄下需有 pw_module.py
    - 在終端機 (command line) 中執行：  python main.py
"""
from 封裝過後的資料格式 import PWInput
from 主要計算程式 import (
    compute_precipitable_water
)

def main():
    print("===== 輸入多筆 (p, c) 資料 =====")
    print("請輸入壓力 (hPa) 與溫度 (°C)，例如：900 25")
    print("直接按 Enter (不輸任何值) 表示結束輸入。")

    data_points = []
    while True:
        line = input("輸入 p, c (空白分隔) 或按 Enter 結束: ").strip()
        if not line:
            break
        try:
            p_str, c_str = line.split()
            p_val = float(p_str)
            c_val = float(c_str)
            data_points.append((p_val, c_val))
        except:
            print("[警告] 格式錯誤，請再試一次。")
            continue

    if len(data_points) < 2:
        print("\n[警告] 至少需要 2 筆 (p, c) 資料才能進行積分，程式終止。")
        return

    print("\n===== 請輸入欲積分的壓力上下邊界 (h1, h2) =====")
    print("例如：1000 500  -> 代表積分範圍 1000hPa 到 500hPa")
    h_input = input("h1, h2: ").strip()
    try:
        h1_str, h2_str = h_input.split()
        h1_val = float(h1_str)
        h2_val = float(h2_str)
    except:
        print("[警告] 格式錯誤，請確認輸入，如：1000 500")
        return

    # 1. 建立 PWInput
    input_data = PWInput(data_points=data_points, h1=h1_val, h2=h2_val)

    # 2. 呼叫計算函式
    result = compute_precipitable_water(input_data)

    # 3. 顯示結果 (PWOutput)
    print("\n===== 每筆 (p, c) 對應 '水氣壓(e)' 與 '比濕度(H_s)' =====")
    for (p_i, c_i, e_i, hs_i) in result.data_details:
        print(f"  p={p_i:7.2f} hPa,  c={c_i:6.2f} °C,  e={e_i:7.3f} hPa,  H_s={hs_i:7.3f} g/kg")

    print("\n===== 分段積分詳情 =====")
    for i, seg in enumerate(result.segment_details, 1):
        print(
            f"  段{i}:  p1={seg['p1']:.2f}, p2={seg['p2']:.2f},"
            f" H_s1={seg['H_s1']:.3f}, H_s2={seg['H_s2']:.3f},"
            f" mean_H_s={seg['mean_H_s'] if 'mean_H_s' in seg else (seg['H_s1']+seg['H_s2'])/2.0:.3f},"
            f" Δp={seg['Δp']:.2f}, area={seg['area']:.3f}"
        )

    print("\n===== 最終結果 =====")
    print(f"  在壓力 {h1_val:.2f} hPa 與 {h2_val:.2f} hPa 之間，")
    print(f"  total_integral = {result.total_integral:.4f} (H_s×hPa)")
    print(f"  可降水量 W_p = {result.W_p:.4f} mm")
    print("=================================\n")

if __name__ == "__main__":
    main()