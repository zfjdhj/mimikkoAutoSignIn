# -*- coding: UTF-8 -*-
"""
 * @author  zfj
 * @date  2020/9/26 15:39
"""
import sys
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    if len(sys.argv)>1:
        app_id = sys.argv[1]
        Authorization=sys.argv[2]
    else:
        print("缺少必要参数！！！(Bot插件版忽略此错误)")
except Exception as e:
    print(e)



# id=sys.argv[3]
# password=sys.argv[4]

apiPath = 'http://api1.mimikko.cn/client/user/GetUserSignedInformation'
apiPath2 = 'http://api1.mimikko.cn/client/dailysignin/log/30/0'
# post_data = {"password": password, "id": id}
sign_path = 'https://api1.mimikko.cn/client/RewardRuleInfo/SignAndSignInformationV3'
energy_info_path = 'https://api1.mimikko.cn/client/love/GetUserServantInstance'
energy_reward_path = 'https://api1.mimikko.cn/client/love/ExchangeReward'

def apiRequest(url,app_id,Authorization,params):
    params_get = params
    headers_get = {
        'Cache-Control': 'Cache-Control:public,no-cache',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'Mozilla/5.0(Linux;Android6.0.1;MuMu Build/V417IR;wv)AppleWebKit/537.36(KHTML,'
                      'like Gecko)Version/4.0 Chrome/52.0.2743.100MobileSafari / 537.36',
        'AppID': app_id,
        'Version': '3.1.2',
        'Authorization': Authorization,
        'Connection': 'Keep-Alive',
        'Host': 'api1.mimikko.cn'
    }
    headers_post = {
        'Accept': 'application/json',
        'Cache-Control': 'no-cache',
        'AppID': app_id,
        'Version': '3.1.2',
        'Content-Type': 'application/json',
        'Host': 'api1.mimikko.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.1',
    }

    try:
        with requests.get(url, headers=headers_get, params=params_get, verify=False, timeout=300) as resp:
            res = resp.json()
            return res

    except Exception as ex:
        print(ex)


# code=momona,ServantName=梦梦奈
# code=ruri,ServantName=琉璃
# code=nemuri,ServantName=奈姆利
# code=miruku2,ServantName=米露可


def mimikko(app_id,Authorization):
    sign_data = apiRequest(sign_path,app_id,Authorization,"")
    energy_info_data = apiRequest(energy_info_path,app_id,Authorization,{"code": "ruri"})
    if energy_info_data:
        if energy_info_data['body']['Energy'] > 0:
            energy_reward_data = apiRequest(energy_reward_path, app_id,Authorization,{"code": "ruri"})
        else:
            energy_reward_data = "您的能量值不足，无法兑换"
    else:
        energy_reward_data = "您的能量值不足，无法兑换"
    sign_info = apiRequest(apiPath, app_id,Authorization, "")
    sign_history = apiRequest(apiPath2, app_id,Authorization, "")
    return sign_data, energy_info_data, energy_reward_data, sign_info, sign_history

def timeStamp2time(timeStamp):
    timeArray = time.localtime(timeStamp/1000)
    otherStyleTime = time.strftime("%m月%d日 %H:%M", timeArray)
    return otherStyleTime


sign_data, energy_info_data, energy_reward_data, sign_info, sign_history = mimikko(app_id,Authorization)
# # sign_data
print('sign_data', sign_data)
# print("code", sign_data["code"])
# # print(sign_data["body"]["date"])
# # print(sign_data["body"]["signTime"])
# print("Name", sign_data["body"]["Name"])
# print('Description', sign_data["body"]['Description'])
# print('PictureUrl', sign_data["body"]['PictureUrl'])
# print('成长值Reward', sign_data["body"]['Reward'])
# print('硬币GetCoin', sign_data["body"]['GetCoin'])
# # Energy info
print('energy_info_data', energy_info_data)
# print('code', energy_info_data['code'])
# print('msg', energy_info_data['msg'])
# # print('Favorability',energy_data['body']['Favorability'])
# # print('MaxFavorability',energy_data['body']['MaxFavorability'])
# print('Favorability/MaxFavorability',
#       str(energy_info_data['body']['Favorability']) + "/" + str(energy_info_data['body']['MaxFavorability']))
# print('Energy', energy_info_data['body']['Energy'])
# # Energy reward
print(energy_reward_data)
# # sign_info
# print(sign_info)
# print(sign_info['code'])
# print('IsSign', sign_info['body']['IsSign'])
# print('连续登录天数ContinuousSignDays', sign_info['body']['ContinuousSignDays'])
# # sign_history
print(sign_history)
# print('code', sign_history['code'])
# print('startTime', timeStamp2time(sign_history["body"]['startTime']))
# print('endTime', timeStamp2time(sign_history["body"]['endTime']))
# print('signLogs', sign_history['body']['signLogs'])
# for item in sign_history['body']['signLogs']:
#     print('signTime', timeStamp2time(item['signDate']))
