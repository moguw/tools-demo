import subprocess,sys,json,time
from datetime import datetime
import path_setting
 
test_env = sys.argv[1]

def playwright():
      start = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 
      test_datas_1 = {
                  "Operation": "Playwright",
                  'Identifier ID / URLs': '-',
                  "Result": "Testing, Wait one moment",
                  "Nickname": "-",
                  "Platform": test_env,
                  'Execution Time':start
            }
      with open('record.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
      if not isinstance(test_datas_1, list):
            test_datas_1 = [test_datas_1]
      updated_data = test_datas_1 + data
      with open("record.json","w", encoding='utf-8') as f:
            json.dump(updated_data,f,indent=4,ensure_ascii=False)

      playwright_path_value = path_setting.get_playwright_path()
      shells_parametrize = "cd %s/playwright-testing-kawo-project &&  rm -rf my-allure-results && npm run %s"%(playwright_path_value,test_env)
      if test_env != 'local':
            print("choose local env")
      else:
            print(subprocess.call(shells_parametrize,shell=True))
            end = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 
            time1 = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            time2 = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            diff = time2-time1
            total_seconds = int(diff.total_seconds())

            # 计算小时、分钟和秒
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # 格式化为 "xh ym zs"
            time_diff_str = ""

            # 添加小时部分（如果大于0）
            if hours > 0:
                  time_diff_str += f"{hours}h "

            # 添加分钟部分（如果大于0）
            if minutes > 0:
                  time_diff_str += f"{minutes}m "

            # 添加秒部分（始终添加）
            time_diff_str += f"{seconds}s"
            file_path = f"{playwright_path_value}/playwright-testing-kawo-project/summary.json"
            with open(file_path,"r", encoding='utf-8') as f:
                  datas = json.load(f)
                  # print(len(data['failed']))
            test_datas_2 = {
                  "Operation": "Playwright",
                  'Identifier ID / URLs': '-', 
                  "Result": "%s Test Done, %s used, %s Failed ❌ "%(len(datas['passed']+datas['warned']+datas['skipped']+datas['timedOut']+datas['flakey']+datas["interrupted"]),time_diff_str,len(datas['failed'])),
                  "Nickname": "-",
                  "Platform": test_env,
                  'Execution Time':start
            }
            
            with open('record.json', 'r', encoding='utf-8') as file:
                  data = json.load(file)
            # if not isinstance(test_datas_2, list):
            #       test_datas_2 = [test_datas_2]
            if data and isinstance(data, list):
                  for i, entry in enumerate(data):
                        if entry["Operation"] == "Playwright" and entry["Result"] == "Testing, Wait one moment":
                              data[i] = test_datas_2
                              break
            # updated_data = test_datas_2 + data
            with open("record.json","w", encoding='utf-8') as f:
                  json.dump(data,f,indent=4,ensure_ascii=False)


if __name__ == "__main__":
    playwright()
        







