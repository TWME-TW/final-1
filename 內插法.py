
def interpolate_point(p_target, p1, p2, H_s1, H_s2):
    """
    在 p1, p2 間，針對 p_target 做 H_s 的線性內插。
    """
    return H_s1 + (H_s2 - H_s1) * ((p_target - p1) / (p2 - p1))