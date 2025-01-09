import customtkinter as ctk
from pw_module import PWInput, compute_precipitable_water

class PWApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Precipitable Water Calculator")
        self.geometry("600x400")

        self.data_points = []

        self.create_widgets()

    def create_widgets(self):
        self.label_instruction = ctk.CTkLabel(self, text="輸入壓力 (hPa) 與溫度 (°C)，例如：900 25")
        self.label_instruction.pack(pady=10)

        self.entry_pc = ctk.CTkEntry(self, placeholder_text="p, c")
        self.entry_pc.pack(pady=5)

        self.button_add = ctk.CTkButton(self, text="新增資料點", command=self.add_data_point)
        self.button_add.pack(pady=5)

        self.label_data_points = ctk.CTkLabel(self, text="目前資料點：")
        self.label_data_points.pack(pady=10)

        self.text_data_points = ctk.CTkTextbox(self, height=100)
        self.text_data_points.pack(pady=5)

        self.label_h = ctk.CTkLabel(self, text="輸入欲積分的壓力上下邊界 (h1, h2)，例如：1000 500")
        self.label_h.pack(pady=10)

        self.entry_h = ctk.CTkEntry(self, placeholder_text="h1, h2")
        self.entry_h.pack(pady=5)

        self.button_calculate = ctk.CTkButton(self, text="計算", command=self.calculate)
        self.button_calculate.pack(pady=10)

        self.text_result = ctk.CTkTextbox(self, height=150)
        self.text_result.pack(pady=5)

    def add_data_point(self):
        line = self.entry_pc.get().strip()
        if not line:
            return
        try:
            p_str, c_str = line.split()
            p_val = float(p_str)
            c_val = float(c_str)
            self.data_points.append((p_val, c_val))
            self.text_data_points.insert(ctk.END, f"p={p_val}, c={c_val}\n")
            self.entry_pc.delete(0, ctk.END)
        except:
            self.text_data_points.insert(ctk.END, "[警告] 格式錯誤，請再試一次。\n")

    def calculate(self):
        if len(self.data_points) < 2:
            self.text_result.insert(ctk.END, "[警告] 至少需要 2 筆 (p, c) 資料才能進行積分，程式終止。\n")
            return

        h_input = self.entry_h.get().strip()
        try:
            h1_str, h2_str = h_input.split()
            h1_val = float(h1_str)
            h2_val = float(h2_str)
        except:
            self.text_result.insert(ctk.END, "[警告] 格式錯誤，請確認輸入，如：1000 500\n")
            return

        input_data = PWInput(data_points=self.data_points, h1=h1_val, h2=h2_val)
        result = compute_precipitable_water(input_data)

        self.text_result.insert(ctk.END, "\n===== 每筆 (p, c) 對應 '水氣壓(e)' 與 '比濕度(H_s)' =====\n")
        for (p_i, c_i, e_i, hs_i) in result.data_details:
            self.text_result.insert(ctk.END, f"  p={p_i:7.2f} hPa,  c={c_i:6.2f} °C,  e={e_i:7.3f} hPa,  H_s={hs_i:7.3f} g/kg\n")

        self.text_result.insert(ctk.END, "\n===== 分段積分詳情 =====\n")
        for i, seg in enumerate(result.segment_details, 1):
            self.text_result.insert(ctk.END, f"  段{i}:  p1={seg['p1']:.2f}, p2={seg['p2']:.2f},"
                                             f" H_s1={seg['H_s1']:.3f}, H_s2={seg['H_s2']:.3f},"
                                             f" mean_H_s={seg['mean_H_s'] if 'mean_H_s' in seg else (seg['H_s1']+seg['H_s2'])/2.0:.3f},"
                                             f" Δp={seg['Δp']:.2f}, area={seg['area']:.3f}\n")

        self.text_result.insert(ctk.END, "\n===== 最終結果 =====\n")
        self.text_result.insert(ctk.END, f"  在壓力 {h1_val:.2f} hPa 與 {h2_val:.2f} hPa 之間，\n")
        self.text_result.insert(ctk.END, f"  total_integral = {result.total_integral:.4f} (H_s×hPa)\n")
        self.text_result.insert(ctk.END, f"  可降水量 W_p = {result.W_p:.4f} mm\n")
        self.text_result.insert(ctk.END, "=================================\n")

if __name__ == "__main__":
    app = PWApp()
    app.mainloop()
