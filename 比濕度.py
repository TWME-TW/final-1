def calc_mixing_ratio(e, p):
    """
    計算比濕度 H_s = 622 * e / p
    e, p (hPa)
    回傳值單位 ~ g/kg
    """
    return 622.0 * e / p