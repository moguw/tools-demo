# # example.py
# import sys
# a = int(sys.argv[1])
# b = int(sys.argv[2])
# def multiply(a, b):
#     return a * b

# if __name__ == "__main__":
#     multiply(a,b)

import requests,sys,time,json,time
homeUrl = sys.argv[1]
platform = sys.argv[2]
opType = sys.argv[3]
headersInfo ={'key': "vdpidii6pcmvdd1mcdkd9cfxc"}
list_url = homeUrl.split(",")


def apiRequest(urls):
    try: 
        response = requests.post(url=urls,headers=headersInfo)      
    except TimeoutError:
        print('API Request Timeout',flush=1)
        sys.stdout.flush()
    else:
        return response

def handAccounts():
    match platform:
        case 'bilibili':
            for i in range(len(list_url)):
                try:
                    #Get bilibili account's identifier value
                    bilibili_identifer_url = 'https://api.newrank.cn/api/v2/custom/bz/kewo/get/uid?homeUrl=%s'%list_url[i]
                    bilibili_identifer_response = apiRequest(bilibili_identifer_url)
                    bilibili_identifier_msg = bilibili_identifer_response.json()['msg']
                    bilibilii_dentifier_id = bilibili_identifer_response.json()['data']['identifier']
                    print(">>"*5,flush=True)
                    print('bilibili_identifier_msg:',bilibili_identifier_msg,'bilibilii_dentifier_id:',bilibilii_dentifier_id,flush=1)
                    sys.stdout.flush()
                    time.sleep(1)
                except:
                    print(">>"*5,flush=True)
                    print("检查你的account,请重新输入!!,",flush=1)
                    sys.stdout.flush()
                    datas = {
                            "Operation":"Add Account",
                            'Identifier ID / URLs':list_url[i],
                            'Result':'获取identifier失败',
                            'Nickname':'null',
                            'Platform':'%s账号异常'%platform,
                            'Execution Time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                            }
                    # datas = [{"identifier_msg:"+identifier_msg, 'identifier:'+identifier,'handle_msg:'+handle_msg,'verify_msg:'+verify_msg,"nickname:"+nickname,'successful,congratulations!!'}]
                    with open('record.json', 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    if not isinstance(datas, list):
                        datas = [datas]

                    updated_data = datas + data

                    print(datas,flush=True)
                    sys.stdout.flush()
                    with open("record.json","w", encoding='utf-8') as f:
                        json.dump(updated_data,f,indent=4,ensure_ascii=False)
                    continue
                try:
                    #add/delete blibili accounts
                    bilibili_handle_url = 'https://api.newrank.cn/api/v2/custom/bz/kewo/account/manage?identifier=%s&opType=%s'%(bilibilii_dentifier_id,opType)
                    bilibili_handle_response = apiRequest(bilibili_handle_url)
                    bilibili_handle_msg = bilibili_handle_response.json()['msg']
                    print('bilibili_handle_msg:',bilibili_handle_msg,flush=1)
                    sys.stdout.flush()
                    time.sleep(1)
                except:
                    print("handle bilibili accounts failed!!",flush=1)
                    sys.stdout.flush()
                try:
                    #check add/delete bilibili account‘s results
                    bilibili_verify_url = 'https://api.newrank.cn/api/v2/custom/bz/kewo/account/list?identifier=%s'%(bilibilii_dentifier_id)
                    bilibili_verify_response = apiRequest(bilibili_verify_url)
                    if opType == 'add':
                        bilibili_verify_msg =  bilibili_verify_response.json()['msg']
                        try:
                            bilibili_nickname = bilibili_verify_response.json()['data']['list'][0]['nickname']
                        except:
                            bilibili_nickname = "null"
                            print("No nickname has been obtained yet,please wait a moment",flush=1)
                            sys.stdout.flush()
                    else:
                        bilibili_nickname = bilibilii_dentifier_id
                        bilibili_verify_msg =  bilibili_verify_response.json()['msg']
                    datas = {  
                            "Operation":"Add Account",
                            'Identifier ID / URLs':bilibilii_dentifier_id,
                            'Result':bilibili_handle_msg,
                            'Nickname':bilibili_nickname,
                            'Platform':platform,
                            'Execution Time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                    }
                    with open('record.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                    if not isinstance(datas, list):
                            datas = [datas]

                    updated_data = datas + data
                    print(datas,flush=1)
                    sys.stdout.flush()
                    with open("record.json","w", encoding='utf-8') as f:
                        json.dump(updated_data,f,indent=4,ensure_ascii=False)
                except:
                    print("Can't get bilibili accounts data result",flush=1)
                    sys.stdout.flush()
                    error_datas = {
                                    "Operation":"Add Account",
                                    'Identifier ID / URLs':list_url[i],
                                    'Result':'null',
                                    'Nickname':'null',
                                    'Platform':"%s账号异常"%platform,
                                    'Execution Time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                           }
                    with open('record.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                    with open('record.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                    if not isinstance(error_datas, list):
                            error_datas = [error_datas]
                    updated_data = error_datas + data
                    with open("record.json","w", encoding='utf-8') as f:
                            json.dump(updated_data,f,indent=4,ensure_ascii=False)
        case 'wx':
            for i in range(len(list_url)):
                try:
                    wx_handle_url = 'https://api.newrank.cn/api/custom/kewo/monitor-account/manage?identifier=%s&opType=%s&platform=%s'%(list_url[i],opType,platform)
                    response = apiRequest(wx_handle_url)
                    wx_handle_msg = response.json()['msg']
                    print(">>"*5,flush=True)
                    print('wx_handle_msg:',wx_handle_msg,flush=1)
                    sys.stdout.flush()
                    time.sleep(1)
                    wx_verify_url = 'https://api.newrank.cn/api/custom/kewo/monitor-account/list?platform=%s&size=10&page=1&identifier=%s'%(platform,list_url[i])
                    response = apiRequest(wx_verify_url)
                    if opType == 'add':
                        wx_verify_msg =  response.json()['msg']
                        wx_nickname = response.json()['data']['list'][0]['nickname']
                    else:
                        wx_nickname = list_url[i]
                        wx_verify_msg =  response.json()['msg']
                    datas = {
                                "Operation":"Add Account",
                                "Identifier ID / URLs":list_url[i],
                                'Result:':wx_handle_msg,
                                'Nickname:':wx_nickname,
                                'Platform': platform,
                                'Execution Time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())   
                    }
                    with open('record.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                    if not isinstance(datas, list):
                            datas = [datas]

                    updated_data = datas + data
                    print(datas,flush=1)
                    sys.stdout.flush()
                    with open("record.json","w", encoding='utf-8') as f:
                        json.dump(updated_data,f,indent=4,ensure_ascii=False)
                except:
                    print(">>"*5,flush=True)
                    print("Can't get weChat accounts data result",flush=1)
                    sys.stdout.flush()
                    error_datas = {
                                    "Operation":"Add Account",
                                    'Identifier ID / URLs':list_url[i],
                                    'Result':'null',
                                    'Nickname':'null',
                                    'Platform':"%s账号异常"%platform,
                                    'Execution Time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                           }
                    with open('record.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                    if not isinstance(error_datas, list):
                            error_datas = [error_datas]
                    updated_data = error_datas + data
                    with open("record.json","w", encoding='utf-8') as f:
                            json.dump(updated_data,f,indent=4,ensure_ascii=False)

        case _:
                for i in range(len(list_url)):
                    try:
                        url = 'https://api.newrank.cn/api/custom/kewo/uid/get?homeUrl=%s&platform=%s'%(list_url[i],platform)
                        url_response = apiRequest(url)
                        identifier_msg = url_response.json()['msg']
                        identifier = url_response.json()['data']['identifier']
                        print(">>"*5,flush=True)
                        print('identifier_msg:',identifier_msg,'identifier:',identifier,flush=True)
                        time.sleep(1)
                        sys.stdout.flush()
                    except:    
                        print(">>"*5,flush=True)
                        print("检查你的account,请重新输入!!",flush=True)
                        sys.stdout.flush()
                        datas = {
                                    "Operation":"Add Account",
                                    'Identifier ID / URLs':list_url[i],
                                    'Result':'获取identifier失败',
                                    'Nickname':'null',
                                    'Platform':'%s账号异常'%platform,
                                    'Execution Time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                            }
                        # datas = [{"identifier_msg:"+identifier_msg, 'identifier:'+identifier,'handle_msg:'+handle_msg,'verify_msg:'+verify_msg,"nickname:"+nickname,'successful,congratulations!!'}]
                        with open('record.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                        if not isinstance(datas, list):
                            datas = [datas]

                        updated_data = datas + data

                        print(datas,flush=True)
                        sys.stdout.flush()
                        with open("record.json","w", encoding='utf-8') as f:
                            json.dump(updated_data,f,indent=4,ensure_ascii=False)
                        continue
                        
                    try:
                        handle_url = 'https://api.newrank.cn/api/custom/kewo/monitor-account/manage?identifier=%s&opType=%s&platform=%s'%(identifier,opType,platform)
                        handle_url_response = apiRequest(handle_url)
                        handle_msg = handle_url_response.json()['msg']
                        print('handle_msg:',handle_msg,flush=True)
                        time.sleep(1)
                        sys.stdout.flush()
                    except:
                        print("handle your accounts failed!!",flush=True)
                        sys.stdout.flush()

                    try:
                        verify_url = 'https://api.newrank.cn/api/custom/kewo/monitor-account/list?platform=%s&size=10&page=1&identifier=%s'%(platform,identifier)
                        verify_url_response = apiRequest(verify_url)
                        if opType == 'delete' or platform == 'sph': 
                            verify_msg = verify_url_response.json()['msg']
                            nickname = list_url[i]
                            identifier = identifier[-12:]
                        else:
                            verify_msg = verify_url_response.json()['msg']
                            try:
                                nickname = verify_url_response.json()['data']['list'][0]['nickname']
                            except:
                                nickname = 'null'
                                print("No nickname has been obtained yet,please wait a moment",flush=True)
                                sys.stdout.flush()
                        datas = {
                                    "Operation":"Add Account",
                                    'Identifier ID / URLs':identifier,
                                    'Result':handle_msg,
                                    'Nickname':nickname,
                                    'Platform':platform,
                                    'Execution Time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                            }
                        # datas = [{"identifier_msg:"+identifier_msg, 'identifier:'+identifier,'handle_msg:'+handle_msg,'verify_msg:'+verify_msg,"nickname:"+nickname,'successful,congratulations!!'}]
                        with open('record.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                        if not isinstance(datas, list):
                            datas = [datas]

                        updated_data = datas + data

                        print(datas,flush=True)
                        sys.stdout.flush()
                        with open("record.json","w", encoding='utf-8') as f:
                            json.dump(updated_data,f,indent=4,ensure_ascii=False)
                    except:
                        print("Can't get your accounts data result",flush=True)
                        sys.stdout.flush()
                        error_datas = {
                                    "Operation":"Add Account",
                                    'Identifier ID / URLs':list_url[i],
                                    'Result':'null',
                                    'Nickname':'null',
                                    'Platform':"%s账号异常"%platform,
                                    'Execution Time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                           }
                        with open('record.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                        if not isinstance(error_datas, list):
                            error_datas = [error_datas]
                        updated_data = error_datas + data
                        with open("record.json","w", encoding='utf-8') as f:
                                json.dump(updated_data,f,indent=4,ensure_ascii=False)


if __name__ == "__main__":
    handAccounts()