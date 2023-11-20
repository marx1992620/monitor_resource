import psutil
import time
import csv
import argparse
from datetime import datetime
import os
import json

def monitor_resource_usage(duration=60, tick=1, output_file='resource_usage.csv' , threshold=1):
    start_time = time.time()
    time_list =[]
    memory_usage = []
    cpu_usage = []
    # 存儲每個進程的CPU和RAM使用率
    resource_percentages = {}

    while time.time() - start_time < duration:
        # 獲取系統虛擬記憶體使用率
        virtual_memory = psutil.virtual_memory()
        memory_usage.append(virtual_memory.percent)
        total_cpu_percent = round(psutil.cpu_percent(), 2)
        cpu_usage.append(total_cpu_percent)
        print(f"System CPU Usage: {total_cpu_percent}% , System Memory Usage: {virtual_memory.percent:.2f}%")
        # 獲取所有正在運行的進程
        processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
        time_list.append(str(datetime.now().strftime("%H:%M:%S")))

        # 更新每個進程的CPU和RAM使用率
        for process in processes:
            try:
                pid = process.info['pid']
                name = process.info['name']
                cpu_percent = round(process.info['cpu_percent'],1)
                ram_percent = round(process.info['memory_percent'],1)

                # 更新最高CPU和RAM占用率
                if pid not in resource_percentages and str(pid) != str(0):
                    resource_percentages[pid] = {'name': name, 'cpu_percent': [],'ram_percent': []}
                    if len(time_list) -1 > 0:
                        resource_percentages[pid]['cpu_percent'].extend([0 for _ in range(len(time_list)-1)])
                        resource_percentages[pid]['ram_percent'].extend([0 for _ in range(len(time_list)-1)])
                        
                if pid in resource_percentages:
                    resource_percentages[pid]['cpu_percent'].append(cpu_percent)
                    resource_percentages[pid]['ram_percent'].append(ram_percent)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # 處理異常情況，例如進程不存在、無法訪問、為殭屍進程等
                pass

        time.sleep(tick)  # 等待1秒再繼續監測

    # 寫入CSV檔案
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["processID_name", "Maximum (%)"] + time_list)
        writer.writerow(["Total_CPU_usage", max(cpu_usage)] + cpu_usage)
        writer.writerow(["Total_RAM_usage", max(memory_usage)] + memory_usage)
        
        for pid in resource_percentages:
            if max(resource_percentages[pid]['cpu_percent']) <threshold and max(resource_percentages[pid]['ram_percent']) <threshold:
                continue
            else:
                writer.writerow([f"{pid}_{resource_percentages[pid]['name']}_cpu"] + [max(resource_percentages[pid]['cpu_percent'])] + resource_percentages[pid]['cpu_percent'])
                writer.writerow([f"{pid}_{resource_percentages[pid]['name']}_ram"] + [max(resource_percentages[pid]['ram_percent'])] +resource_percentages[pid]['ram_percent'])




def main():
    if os.path.exists("record_cpu.json"):
        with open("record_cpu.json","r",encoding="utf8")as f:
            arguments = json.loads(f.read())
            monitor_resource_usage(duration=arguments["duration"], tick=arguments["tick"], output_file=arguments["output"], threshold=arguments["threshold"])

    else:
        parser = argparse.ArgumentParser(description='Monitor resource usage of processes.')
        parser.add_argument('--duration', type=int, default=60, help='Duration of monitoring in seconds.')
        parser.add_argument('--tick', type=int, default=1, help='Every tick to query cpu and ram')
        parser.add_argument('--output', default='resource_usage.csv', help='Output CSV file name.')
        parser.add_argument('--threshold', type=int, default=1, help='threshold to filter data')
        args = parser.parse_args()
        monitor_resource_usage(duration=args.duration, tick=args.tick, output_file=args.output, threshold=args.threshold)

if __name__ == "__main__":
    print("start")
    main()
    print("done")
    x = input()
