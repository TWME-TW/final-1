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