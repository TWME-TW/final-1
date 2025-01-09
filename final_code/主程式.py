from 計算蒸氣壓 import calculate_vapor_pressure
from 計算比濕度 import calculate_specific_humidity
from 計算可降水量 import calculate_precipitable_water

# 主程式
def main():
    # Step 1: 輸入壓力和溫度數據
    print("請輸入壓力 p 和對應溫度 c (格式: p1,c1 p2,c2 ...)，以空格分隔:")
    input_data = input()
    data_points = input_data.split()
    
    pressures = []
    temperatures = []
    
    for point in data_points:
        p, c = map(float, point.split(","))
        pressures.append(p)
        temperatures.append(c)
    
    # 計算蒸氣壓
    vapor_pressures = calculate_vapor_pressure(pressures, temperatures)
    
    # 計算比濕度
    specific_humidity = calculate_specific_humidity(vapor_pressures, pressures)
    
    # 計算壓力差
    pressure_differences = [abs(pressures[i] - pressures[i + 1]) for i in range(len(pressures) - 1)]
    
    # 計算平均比濕度
    average_specific_humidity = [(specific_humidity[i] + specific_humidity[i + 1]) / 2 for i in range(len(specific_humidity) - 1)]
    
    # 計算可降水量
    precipitable_water = calculate_precipitable_water(pressure_differences, average_specific_humidity)
    
    # 顯示結果
    print("\n計算結果:")
    for i, (p, c, e, H) in enumerate(zip(pressures, temperatures, vapor_pressures, specific_humidity), start=1):
        print(f"點{i}: 壓力={p}mb, 溫度={c}°C, 蒸氣壓={e:.2f}mb, 比濕度={H:.2f}g/kg")
    
    for i, (p_diff, H_avg) in enumerate(zip(pressure_differences, average_specific_humidity), start=1):
        print(f"壓力差{i}={p_diff}mb, 平均比濕度{i}={H_avg:.2f}g/kg")
    
    print(f"\n可降水量 W_p={precipitable_water:.2f} mm")

# 執行主程式
if __name__ == "__main__":
    main()