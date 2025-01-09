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