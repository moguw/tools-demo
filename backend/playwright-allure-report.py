import subprocess,sys,time,json
from datetime import datetime
import path_setting
playwright_path_value = path_setting.get_playwright_path()
shells_parametrize = "allure generate %s/playwright-testing-kawo-project/my-allure-results  --clean -o allure-report"%playwright_path_value
def playwrightReport():
        print(subprocess.call(shells_parametrize,shell=True)) 
        file_path = f"{playwright_path_value}/playwright-testing-kawo-project/summary.json"
        with open(file_path, 'r', encoding='utf-8') as f:
            datas_summary = json.load(f) 
        with open('record.json', 'r', encoding='utf-8') as f:
            datas_record = json.load(f)

        # 过滤出 Operation 为 Playwright 的记录
        playwright_operations = [item for item in datas_record if item["Operation"] == "Playwright"]

        # 找到 Execution Time 最新的那条记录
        if playwright_operations:
            latest_operation = max(playwright_operations, key=lambda x: datetime.strptime(x["Execution Time"], '%Y-%m-%d %H:%M:%S'))
            # print(f"最新的 Operation 为 Playwright 的记录: {latest_operation['Identifier ID / URLs / ENV']}")
        else:
            print("没有找到 Operation 为 Playwright 的记录")
        test_datas = {
                "Operation":"Generate Report",
                'Identifier ID / URLs':'-',
                "Result": "%s failed"%len(datas_summary['failed']),
                "Nickname": "-",
                "Platform": latest_operation['Platform'],
                'Execution Time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            }
        with open('record.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        if not isinstance(test_datas, list):
                test_datas = [test_datas]
        updated_data = test_datas + data
        with open("record.json","w", encoding='utf-8') as f:
                    json.dump(updated_data,f,indent=4,ensure_ascii=False)
               




if __name__ == "__main__":
    playwrightReport()
        

# import subprocess
# import time
# import signal
# import os

# def start_allure_server(results_path):
#     # 启动 allure serve 并捕获进程对象
#     process = subprocess.Popen(['allure', 'serve', results_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     return process

# def stop_allure_server(process):
#     # 终止 allure serve 进程
#     process.terminate()
#     try:
#         # 等待进程终止
#         process.wait(timeout=10)
#     except subprocess.TimeoutExpired:
#         # 如果进程没有在10秒内终止，强制终止
#         os.kill(process.pid, signal.SIGKILL)
#         process.wait()

# def main():
#     results_path = '/Users/nan/Desktop/new_last_1/playwright-testing-kawo-project/my-allure-results'
#     allure_process = start_allure_server(results_path)

#     # 等待一些时间，模拟服务器运行
#     print("Allure server started, running for 10 seconds...")
#     time.sleep(10)

#     stop_allure_server(allure_process)
#     print("Allure server terminated")

# if __name__ == '__main__':
#     main()
