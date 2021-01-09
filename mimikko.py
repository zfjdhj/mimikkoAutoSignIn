# -*- coding: UTF-8 -*-
"""
 * @author  zfj
 * @date  2020/9/26 15:39
"""
import sys
import time
import requests
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    if len(sys.argv)==4:
        app_id = sys.argv[1]
        Authorization = sys.argv[2]
        Energy_code = sys.argy[3]
    elif len(sys.argv)==5:
        app_id = sys.argv[1]
        Authorization = sys.argv[2]
        Energy_code = sys.argy[3]
        SCKEY = sys.argy[4]
    else:
        logging.debug("缺少必要参数！！！(Bot插件版忽略此错误)")
        # 也可以在这里设定默认值
        app_id = ""
        Authorization = ""
        Energy_code = ""
        SCKEY = ""
except Exception as e:
    logging.debug(e)


apiPath = 'http://api1.mimikko.cn/client/user/GetUserSignedInformation' # 今天是否签到
apiPath2 = 'http://api1.mimikko.cn/client/dailysignin/log/30/0' # 签到历史
# post_data = {"password": password, "id": id}
sign_path = 'https://api1.mimikko.cn/client/RewardRuleInfo/SignAndSignInformationV3' # 签到
energy_info_path = 'https://api1.mimikko.cn/client/love/GetUserServantInstance' # 获取助手状态
energy_reward_path = 'https://api1.mimikko.cn/client/love/ExchangeReward' # 兑换助手能量
vip_info = 'https://api1.mimikko.cn/client/user/GetUserVipInfo' # 获取会员状态
vip_roll = 'https://api1.mimikko.cn/client/roll/RollReward' # 会员抽奖
server_api = 'https://sc.ftqq.com/' + SCKEY + '.send'

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
        'Authorization': Authorization,
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
        logging.debug(ex)


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
    sign_data = apiRequest(sign_path,app_id,Authorization,"")
    if sign_data:
        if sign_data.get('body'):
            sign_result_post = '签到成功：\n好感度：' + sign_data['body']['Reward'] + '\n硬币：' + sign_data['body']['GetCoin'] + '\n经验值：' + sign_data['body']['GetExp'] + '\n签到卡片：' + sign_data['body']['Description'] + sign_data['body']['Name'] + '\n' + sign_data['body']['PictureUrl']
        else:
            sign_result_post = '签到失败'
    else:
        sign_result_post = '签到失败'
    vip_info_data = apiRequest(vip_info,app_id,Authorization,"")
    if vip_info_data:
        if vip_info_data.get('body'):
            if vip_info_data['body']['rollNum'] > 0:
                vip_roll_data = apiRequest(vip_roll,app_id,Authorization,"")
                vip_roll_post = "VIP抽奖成功：" + vip_roll_data['body']['Value']['description']
            else:
                vip_roll_data = "抽奖次数不足"
                vip_roll_post = "VIP抽奖失败"
        else:
            vip_roll_data = "抽奖次数不足"
            vip_roll_post = "VIP抽奖失败"
    else:
        vip_roll_data = "抽奖次数不足"
        vip_roll_post = "VIP抽奖失败"
    energy_info_data = apiRequest(energy_info_path,app_id,Authorization,{"code": "Energy_code"})
    if energy_info_data:
        if energy_info_data.get('body'):
            if energy_info_data['body']['Energy'] > 0:
                energy_reward_data = apiRequest(energy_reward_path, app_id,Authorization,{"code": "Energy_code"})
                energy_reward_post = "好感度兑换成功：\n能量值：" + energy_info_data['body']['Energy'] + "/" +energy_info_data['body']['MaxEnergy'] + "\n助手：" + energy_info_data['body']['code']
            else:
                energy_reward_data = "您的能量值不足，无法兑换"
                energy_reward_post = "能量兑换失败"
        else:
            energy_reward_data = "您的能量值不足，无法兑换"
            energy_reward_post = "能量兑换失败"
    else:
        energy_reward_data = "您的能量值不足，无法兑换"
        energy_reward_post = "能量兑换失败"
    sign_info = apiRequest(apiPath, app_id,Authorization, "")
    sign_history = apiRequest(apiPath2, app_id,Authorization, "")
    return sign_data, vip_roll_data, energy_info_data, energy_reward_data, sign_info, sign_history, sign_result_post, vip_roll_post, energy_reward_post

def timeStamp2time(timeStamp):
    timeArray = time.localtime(timeStamp/1000)
    otherStyleTime = time.strftime("%m月%d日 %H:%M", timeArray)
    return otherStyleTime

if app_id and Authorization:
    sign_data, vip_roll_data, energy_info_data, energy_reward_data, sign_info, sign_history, sign_result_post, vip_roll_post, energy_reward_post = mimikko(app_id,Authorization)
    # # sign_data
    logging.debug('sign_data', sign_data)
    # print("code", sign_data["code"])
    # # print(sign_data["body"]["date"])
    # # print(sign_data["body"]["signTime"])
    # print("Name", sign_data["body"]["Name"])
    # print('Description', sign_data["body"]['Description'])
    # print('PictureUrl', sign_data["body"]['PictureUrl'])
    # print('成长值Reward', sign_data["body"]['Reward'])
    # print('硬币GetCoin', sign_data["body"]['GetCoin'])
    # # roll info
    logging.debug('vip_roll_data', vip_roll_data)
    # # Energy info
    logging.debug('energy_info_data', energy_info_data)
    # print('code', energy_info_data['code'])
    # print('msg', energy_info_data['msg'])
    # # print('Favorability',energy_data['body']['Favorability'])
    # # print('MaxFavorability',energy_data['body']['MaxFavorability'])
    # print('Favorability/MaxFavorability',
    #       str(energy_info_data['body']['Favorability']) + "/" + str(energy_info_data['body']['MaxFavorability']))
    # print('Energy', energy_info_data['body']['Energy'])
    # # Energy reward
    logging.debug(energy_reward_data)
    # # sign_info
    # print(sign_info)
    # print(sign_info['code'])
    # print('IsSign', sign_info['body']['IsSign'])
    # print('连续登录天数ContinuousSignDays', sign_info['body']['ContinuousSignDays'])
    # # sign_history
    logging.debug(sign_history)
    # print('code', sign_history['code'])
    # print('startTime', timeStamp2time(sign_history["body"]['startTime']))
    # print('endTime', timeStamp2time(sign_history["body"]['endTime']))
    # print('signLogs', sign_history['body']['signLogs'])
    # for item in sign_history['body']['signLogs']:
    #     print('signTime', timeStamp2time(item['signDate']))
    print('\n' + '\n' +sign_result_post + '\n' + vip_roll_post + '\n' + energy_reward_post)
    if SCKEY:
        post_info = re.sub('\\n', '<br>', sign_result_post + '\n' + vip_roll_post + '\n' + energy_reward_post, count=0, flags=0)
        post_data = requests.post(server_api, data = post_info)
        
