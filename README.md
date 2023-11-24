### 專案名稱

監測各時刻程式CPU、RAM使用率

### 目的

為解決電腦卡頓問題，撰寫一支CPU、RAM監測程式，記錄電腦所有APP的CPU、RAM使用率及最大值，以期優化問題程式之CPU、RAM使用率。

### 操作說明

1. git 下載後內容如下<br>
 ![folder](https://github.com/marx1992620/resource_monitor/blob/main/folder.png)

2. 執行 monitor_cpu_ram.py 前安裝所需 requirements.txt。

   1) 執行程式若同一層資料夾內中有config.json，優先讀取config內參數 { duration:監測總時長，預設60秒、tick:每多少秒監測一次，預設1秒、output:輸出檔名，預設resource_usage.csv、threshold:門檻值，過濾CPU及RAM之最大值，若皆小於門檻值則過濾不輸出檔案，預設1(即1%) }。

   2) 若無config執行時可動態輸入參數(如 python monitor_cpu_ram.py -- duration 30)。

   3) 執行 monitor_cpu_ram.exe，僅會讀取同一層資料夾內的config.json，如無則會照預設值執行。執行畫面如下<br>
 ![processing](https://github.com/marx1992620/resource_monitor/blob/main/process.png)

3. 程式執行完，輸出結果 resource.usage.csv，第二欄為各列數字的最大值，其餘欄位為各時間點；第一二列為電腦總CPU、RAM使用率，其餘列為各程式之CPU、RAM使用率，單位為 % <br>
 ![excel](https://github.com/marx1992620/resource_monitor/blob/main/output.png)
<br>

### 資料說明

CPU總使用率:在測量時間內，計算每個 CPU 平均使用時間，換算成百分比。<br>
各程式CPU使用率:在測量時間內，計算程式占用 CPU 平均使用時間，換算成百分比。
