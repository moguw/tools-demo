# import requests,json
# url =  "https://kawo.sentry.io/issues/?environment=production&project=215896&query=expired&referrer=issue-list&statsPeriod=24h"
# # headers = {"Authorization": "Bearer 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"}
# res = requests.get(url=url)
# print(res.text)

# 有1、2、3、4个数字，能组成多少个互不相同且无重复数字的三位数？都是多少？
# num_list = []
# cou = 0
# for i in range(1,5):
#     for j in range(1,5):
#         for k in range(1,5):
#             if i!=j and j!=k and k!=i:
#                 res=i*100+j*10+k
#                 num_list.append(res)
#                 cou+=1
# print(cou,num_list)
# 一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？

# import math
# num = 1
# while True:
#     if math.sqrt(num + 100)-int(math.sqrt(num + 100)) == 0 and math.sqrt(num + 168)-int(math.sqrt(num + 168)) == 0:
#         print(num)
#         break
#     num += 1

# 输入某年某月某日，判断这一天是这一年的第几天？
# import datetime
# import time
# dtstr = str(input('Enter the datetime:(20151215):'))
# dt = datetime.datetime.strptime(dtstr, "%Y%m%d")
# another_dtstr =dtstr[:4] +'0101'
# another_dt = datetime.datetime.strptime(another_dtstr, "%Y%m%d")
# print (int((dt-another_dt).days) + 1)








