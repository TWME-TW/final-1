from 內插法 import interpolate_point

def integrate_Hs_over_p(data_points, h1, h2):
    """
    利用梯形公式，對在 [h1, h2] 區間的 (p, H_s) 做數值積分。
    
    參數:
        data_points: 內部元素為 (p, H_s) 的列表，p 單位hPa, H_s 單位g/kg
        h1, h2: 積分區間的上下界限，單位hPa
        
    回傳:
        total_integral (float): ∫(H_s dP) 的積分結果
        segment_detail (list of dict): 每分段的詳細資訊
    """
    # 確保積分上下限的順序，使 p_upper > p_lower
    p_upper = max(h1, h2)
    p_lower = min(h1, h2)

    # 將資料點按氣壓(p)從大到小排序
    data_sorted = sorted(data_points, key=lambda x: x[0], reverse=True)

    # 用於存儲在積分區間內的資料點
    clipped = []
    
    # 處理每一對相鄰的資料點
    for i in range(len(data_sorted) - 1):
        # 取得相鄰兩點的座標
        p_a, hs_a = data_sorted[i]      # 第一點的氣壓和比濕
        p_b, hs_b = data_sorted[i+1]    # 第二點的氣壓和比濕

        # 找出這段線段的氣壓範圍
        hi_local = max(p_a, p_b)  # 這段的最高氣壓
        lo_local = min(p_a, p_b)  # 這段的最低氣壓

        # 檢查此線段是否與積分區間有交集
        if hi_local < p_lower or lo_local > p_upper:
            # 無交集，跳過此段
            continue

        # 計算交集區間的上下限
        seg_upper = min(hi_local, p_upper)  # 取較小值作為區段上限
        seg_lower = max(lo_local, p_lower)  # 取較大值作為區段下限

        def get_Hs_at(p_target):
            """
            在給定氣壓值處求得比濕值
            若目標氣壓與已知點重合，直接使用該點的比濕值
            否則進行線性內插
            """
            if abs(p_target - p_a) < 1e-9:     # 使用小數值來比較浮點數
                return hs_a
            elif abs(p_target - p_b) < 1e-9:
                return hs_b
            else:
                return interpolate_point(p_target, p_a, p_b, hs_a, hs_b)

        # 計算交集區間端點的比濕值
        hs_u = get_Hs_at(seg_upper)    # 上限點的比濕
        hs_l = get_Hs_at(seg_lower)    # 下限點的比濕

        # 將交集區間的端點加入列表
        clipped.append((seg_upper, hs_u))
        clipped.append((seg_lower, hs_l))

    # 去除重複的點
    clipped = list(set(clipped))
    # 將點按氣壓從大到小排序
    clipped_sorted = sorted(clipped, key=lambda x: x[0], reverse=True)

    # 計算數值積分
    total_integral = 0.0
    segment_detail = []
    # 對每一個子區間進行梯形法積分
    for i in range(len(clipped_sorted) - 1):
        # 取得區間端點值
        p1, hs1 = clipped_sorted[i]         # 左端點
        p2, hs2 = clipped_sorted[i+1]       # 右端點
        dp = abs(p1 - p2)                   # 氣壓差
        mean_hs = (hs1 + hs2) / 2.0         # 平均比濕
        area = mean_hs * dp                 # 計算此區間的積分值
        total_integral += area              # 累加到總積分
        
        # 記錄此區間的詳細資訊
        segment_detail.append({
            "p1": p1,          # 左端點氣壓
            "p2": p2,          # 右端點氣壓
            "H_s1": hs1,       # 左端點比濕
            "H_s2": hs2,       # 右端點比濕
            "mean_H_s": mean_hs,  # 平均比濕
            "Δp": dp,            # 氣壓差
            "area": area        # 區間積分值
        })

    return total_integral, segment_detail