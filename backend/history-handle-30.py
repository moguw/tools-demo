import json
from datetime import datetime, timedelta

# 读取 JSON 文件内容
with open('record.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 计算30天前的日期
thirty_days_ago = datetime.now() - timedelta(days=30)

# 过滤出 "Execution Time" 在30天之前的记录
filtered_data = [item for item in data if datetime.strptime(item["Execution Time"], '%Y-%m-%d %H:%M:%S') >= thirty_days_ago]

# 将过滤后的数据写回 JSON 文件
with open('file.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

print("过滤后的数据:", filtered_data)
