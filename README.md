# Precipitable Water Calculator

這個專案是一個可降水量 (Precipitable Water, W_p) 計算器，提供圖形使用者介面 (GUI) 和命令列介面 (CLI) 兩種使用方式。使用者可以輸入壓力和溫度數據，並計算在指定壓力範圍內的可降水量。

## 目錄結構

- `gui_main.py`: 提供圖形使用者介面，使用 `customtkinter` 庫。
- `main.py`: 提供命令列介面，示範如何使用 `pw_module.py` 提供的功能。
- `pw_module.py`: 包含計算可降水量的核心模組，包括數據結構和計算函式。
- `README.md`: 專案簡介文件。

## 使用方法

### 圖形使用者介面

執行 `gui_main.py` 來啟動圖形使用者介面：

```sh
python gui_main.py