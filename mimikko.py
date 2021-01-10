# -*- coding: UTF-8 -*-
"""
 * @author  zfj
 * @date  2020/9/26 15:39
"""
import sys
import time
import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    if len(sys.argv)==4 or len(sys.argv)==5:
        app_id = sys.argv[1]
        Authorization = sys.argv[2]
        Energy_code = sys.argv[3]
    else:
        print("缺少必要参数！！！(Bot插件版忽略此错误)")
        # 也可以在这里设定默认值，但请注意账号泄露风险
        app_id = ""
        Authorization = ""
        Energy_code = ""
        SCKEY = ""
except Exception as e:
    print(e)


apiPath = 'http://api1.mimikko.cn/client/user/GetUserSignedInformation' # 今天是否签到
apiPath2 = 'http://api1.mimikko.cn/client/dailysignin/log/30/0' # 签到历史
defeat_set = 'https://api1.mimikko.cn/client/Servant/SetDefaultServant' # 默认助手
sign_path = 'https://api1.mimikko.cn/client/RewardRuleInfo/SignAndSignInformationV3' # 签到
energy_info_path = 'https://api1.mimikko.cn/client/love/GetUserServantInstance' # 获取助手状态
energy_reward_path = 'https://api1.mimikko.cn/client/love/ExchangeReward' # 兑换助手能量
vip_info = 'https://api1.mimikko.cn/client/user/GetUserVipInfo' # 获取会员状态
vip_roll = 'https://api1.mimikko.cn/client/roll/RollReward' # 会员抽奖
server_api = 'https://sc.ftqq.com/'

def apiRequest_get(url,app_id,Authorization,params):
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
    
    try:
        with requests.get(url, headers=headers_get, params=params_get, verify=False, timeout=300) as resp:
            res = resp.json()
            return res

    except Exception as ex:
        print(ex)

def apiRequest_post(url,app_id,Authorization,params):
    params_get = params
    headers_post = {
        'Accept': 'application/json',
        'Cache-Control': 'no-cache',
        'AppID': app_id,
        'Version': '3.1.2',
        'Authorization': Authorization,
        'Content-Type': 'application/json',
        'Host': 'api1.mimikko.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.1',
    }

    try:
        with requests.post(url, headers=headers_get, params=params_get, verify=False, timeout=300) as resp:
            res = resp.json()
            return res

    except Exception as ex:
        print(ex)

# code=nonona,ServantName=诺诺纳
# code=momona,ServantName=梦梦奈
# code=ariana,ServantName=爱莉安娜
# code=miruku,ServantName=米璐库
# code=nemuri,ServantName=奈姆利
# code=ruri,ServantName=琉璃
# code=alpha0,ServantName=阿尔法零
# code=miruku2,ServantName=米露可
# code=ulrica,ServantName=优莉卡


def mimikko(app_id,Authorization):
    defeat_data = apiRequest_get(defeat_set + "?code=" + Energy_code,app_id,Authorization,"")
    sign_data = apiRequest_get(sign_path,app_id,Authorization,"")
    #print(type(sign_data))
    if sign_data:
        if sign_data.get('body'):
            sign_info = apiRequest_get(apiPath, app_id,Authorization, "")
            if sign_info:
                sign_result_post = '签到成功：' + str(sign_info['body']['ContinuousSignDays']) + '天\n好感度：' + str(sign_data['body']['Reward']) + '\n硬币：' + str(sign_data['body']['GetCoin']) + '\n经验值：' + str(sign_data['body']['GetExp']) + '\n签到卡片：' + sign_data['body']['Description'] + sign_data['body']['Name'] + '\n' + sign_data['body']['PictureUrl']
        else:
            sign_result_post = '签到失败'
    else:
        sign_result_post = '签到请求失败'
    vip_info_data = apiRequest_get(vip_info,app_id,Authorization,"")
    if vip_info_data:
        if vip_info_data.get('body'):
            if vip_info_data['body']['rollNum'] > 0:
                vip_roll_data = apiRequest_post(vip_roll,app_id,Authorization,"")
                #print(type(vip_roll_data))
                #print(type(vip_roll_data['body']))
                #print(type(ast.literal_eval(vip_roll_data['body'])['Value']))
                #print(type(vip_roll_data['body']['Value']['description']))
                vip_roll_post = "VIP抽奖成功：" + str(vip_roll_data['body']['Value']['description'])
            else:
                vip_roll_data = "抽奖次数不足"
                if vip_info_data['body']['isValid']:
                    vip_roll_post = "VIP抽奖失败：今天已经抽过奖了"
                else:
                    vip_roll_post = "VIP抽奖失败：您还不是VIP"
        else:
            vip_roll_data = "抽奖次数不足"
            vip_roll_post = "VIP抽奖失败"
    else:
        vip_roll_data = "抽奖次数不足"
        vip_roll_post = "VIP抽奖请求失败"
    energy_info_data = apiRequest_get(energy_info_path + "?code=" + Energy_code,app_id,Authorization,"")
    if energy_info_data:
        if energy_info_data.get('body'):
            if energy_info_data['body']['Energy'] > 0:
                energy_reward_data = apiRequest_get(energy_reward_path + "?code=" + Energy_code, app_id,Authorization,"")
                energy_reward_post = "好感度兑换成功：\n能量值：" + str(energy_info_data['body']['Energy']) + "/" +str(energy_info_data['body']['MaxEnergy']) + "\n助手：" + energy_info_data['body']['code']
            else:
                energy_reward_data = "您的能量值不足，无法兑换"
                energy_reward_post = "能量兑换失败：能量需要＞0"
        else:
            energy_reward_data = "您的能量值不足，无法兑换"
            energy_reward_post = "能量兑换失败"
    else:
        energy_reward_data = "您的能量值不足，无法兑换"
        energy_reward_post = "能量兑换请求失败"
    sign_history = apiRequest_get(apiPath2, app_id,Authorization, "")
    return sign_data, vip_info_data, vip_roll_data, energy_info_data, energy_reward_data, sign_info, sign_history, sign_result_post, vip_roll_post, energy_reward_post

def timeStamp2time(timeStamp):
    timeArray = time.localtime(timeStamp/1000)
    otherStyleTime = time.strftime("%m月%d日 %H:%M", timeArray)
    return otherStyleTime

if app_id and Authorization:
    sign_data, vip_info_data, vip_roll_data, energy_info_data, energy_reward_data, sign_info, sign_history, sign_result_post, vip_roll_post, energy_reward_post = mimikko(app_id,Authorization)
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
    # # roll info
    print('vip_roll_data', vip_roll_data)
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
    print('\n' + '\n' +sign_result_post + '\n' + vip_roll_post + '\n' + energy_reward_post)      
try:
    # print(len(sys.argv))
    if len(sys.argv)==5:
        SCKEY = sys.argv[4]
        # print("有SCKEY")
        print("正在推送到微信")
        post_info = "?text=兽耳助手签到&desp=<p>" + re.sub('\\n', '  \n', sign_result_post + '\n' + vip_roll_post + '\n' + energy_reward_post, count=0, flags=0) + "  \n  \n" + str(sign_data) + "  \n  \n" + str(vip_roll_data) + "  \n  \n" + str(energy_info_data) + "</p>"
        post_data = requests.get(server_api + SCKEY + '.send' + post_info)
        print(post_data)
    else:
        print("没有SCKEY")
except Exception as e:
    print(e)

