import json
def get_playwright_path():
    with open("path_setting.json","r", encoding='utf-8') as f:
            datas = json.load(f)
    return datas['playwright-project-path']
