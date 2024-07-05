import subprocess,sys,json,time
import path_setting
 
test_env = sys.argv[1]

def playwright():
        playwright_path_value = path_setting.get_playwright_path()
        shells_parametrize = "cd %s/playwright-testing-kawo-project &&  rm -rf my-allure-results && npm run %s"%(playwright_path_value,test_env)
        if test_env != 'local':
            print("choose local env")
        else:
            print(subprocess.call(shells_parametrize,shell=True))
            file_path = f"{playwright_path_value}/playwright-testing-kawo-project/summary.json"
            with open(file_path,"r", encoding='utf-8') as f:
                  datas = json.load(f)
                  # print(len(data['failed']))
            test_datas = {
                  "Operation": "Playwright",
                  'Identifier ID / URLs': '-',
                  "Result": "testcase failed:%s"%len(datas['failed']),
                  "Nickname": "-",
                  "Platform": test_env,
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
    playwright()
        







