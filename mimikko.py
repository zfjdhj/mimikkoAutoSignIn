# -*- coding: UTF-8 -*-
"""
 * @author  cyb233
 * @date  2021/1/9
"""
import sys
import time
import requests
import re
import json
import getopt
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
optlist, args = getopt.getopt(sys.argv[1:], 'i:e:l:a:u:p:s:r:')

try:
    for o,a in optlist:
        if o == '-i' and a.strip() != '':
            app_id = a.strip()
        elif o == '-i' :
            sys.exit('读取参数错误！！！')
        if o == '-e' and a.strip() != '':
            Energy_code = a.strip()
        elif o == '-e':
            Energy_code = 'momona'
        if o == '-a' and a.strip() != '':
            Authorization = a.strip()
        elif o == '-a':
            Authorization = False
        if o == '-u' and a.strip() != '':
            user_id = a.strip()
        elif o == '-u':
            user_id = False
        if o == '-p' and a.strip() != '':
            user_password = a.strip()
        elif o == '-p':
            user_password = False
        if o == '-s' and a.strip() != '':
            SCKEY = a.strip()
        elif o == '-s':
            SCKEY = False
        if o == '-r':
            if a.strip() in ['1','2','3','4','5','6','7']:
                resign = a.strip()
            else:
                resign = False
        if o == '-l':
            if a.strip().upper() == 'TRUE':
                login = True
            else:
                login = False
except Exception as e:
    print('传递参数错误：' + e)

login_path = 'https://api1.mimikko.cn/client/user/LoginWithPayload' # 登录(post)
is_sign = 'http://api1.mimikko.cn/client/user/GetUserSignedInformation' # 今天是否签到
history_path = 'http://api1.mimikko.cn/client/dailysignin/log/30/0' # 签到历史
can_resign = 'https://api1.mimikko.cn/client/love/getcanresigntimes' # 补签卡数量
defeat_set = 'https://api1.mimikko.cn/client/Servant/SetDefaultServant' # 设置默认助手
resign_path = 'https://api1.mimikko.cn/client/love/resign?servantId=' # 补签(post)
sign_path = 'https://api1.mimikko.cn/client/RewardRuleInfo/SignAndSignInformationV3' # 签到
energy_info_path = 'https://api1.mimikko.cn/client/love/GetUserServantInstance' # 获取助手状态
energy_reward_path = 'https://api1.mimikko.cn/client/love/ExchangeReward' # 兑换助手能量
vip_info = 'https://api1.mimikko.cn/client/user/GetUserVipInfo' # 获取会员状态
vip_roll = 'https://api1.mimikko.cn/client/roll/RollReward' # 会员抽奖(post)
server_api = 'https://sc.ftqq.com/' # 微信推送
app_Version = '3.1.3'
servant_name = {'nonona':'诺诺纳','momona':'梦梦奈','ariana':'爱莉安娜','miruku':'米璐库','nemuri':'奈姆利','ruri':'琉璃','alpha0':'阿尔法零','miruku2':'米露可','ulrica':'优莉卡'}

def loginRequest_post(url,app_id,app_Version,params):
    params_post = params
    headers_post = {
        'Accept': 'application/json',
        'Cache-Control': 'no-cache',
        'AppID': app_id,
        'Version': app_Version,
        'Content-Type': 'application/json',
        'Host': 'api1.mimikko.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.1',
    }

    try:
        with requests.post(url, headers=headers_post, params=params_post, verify=False, timeout=300) as resp:
            res = resp.json()
            return res

    except Exception as ex:
        print(ex)

def apiRequest_get(url,app_id,app_Version,Authorization,params):
    params_get = params
    headers_get = {
        'Cache-Control': 'Cache-Control:public,no-cache',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'Mozilla/5.0(Linux;Android6.0.1;MuMu Build/V417IR;wv)AppleWebKit/537.36(KHTML,like Gecko)Version/4.0 Chrome/52.0.2743.100MobileSafari / 537.36',
        'AppID': app_id,
        'Version': app_Version,
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

def apiRequest_post(url,app_id,app_Version,Authorization,params):
    params_post = params
    headers_post = {
        'Accept': 'application/json',
        'Cache-Control': 'no-cache',
        'AppID': app_id,
        'Version': app_Version,
        'Authorization': Authorization,
        'Content-Type': 'application/json',
        'Host': 'api1.mimikko.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.1',
    }

    try:
        with requests.post(url, headers=headers_post, params=params_post, verify=False, timeout=300) as resp:
            res = resp.json()
            return res

    except Exception as ex:
        print(ex)

def timeStamp2time(timeStamp):
    timeArray = time.localtime(timeStamp)
    firstStyleTime = time.strftime('%Y-%m-%d', timeArray)
    secondStyleTime = time.strftime('%Y年%m月%d日 %H:%M:%S', timeArray)
    return firstStyleTime, secondStyleTime

def mimikko():
    """
    global Authorization
    #登录
    if login and user_id and user_password:
        login_data = loginRequest_post(login_path,app_id,app_Version,'{"password":"' + user_password + '","id":"' + user_id + '"}')
        if login_data and login_data.get('body'):
            Authorization = login_data['body']['Token']
            print("登录成功！")
        else:
            if Authorization:
                print("登录失败，尝试使用保存的Authorization")
            else:
                sys.exit('登录失败！！！')
    else:
        if login and Authorization:
            print("未找到登录ID或密码，尝试使用保存的Authorization")
        elif login and not Authorization:
            sys.exit('请在Secret中保存登录ID和密码！！！')
        elif not Authorization:
            sys.exit('请在Secret中保存Authorization！！！')
    """
    #设置默认助手
    defeat_data = apiRequest_get(defeat_set + "?code=" + Energy_code,app_id,app_Version,Authorization,"")
    #执行前的好感度
    original_energy_data = apiRequest_get(energy_info_path + "?code=" + Energy_code,app_id,app_Version,Authorization,"")
    if original_energy_data and original_energy_data.get('body'):
        original_energy_post = str(original_energy_data['body']['Favorability'])
    else:
        energy_reward_post = "*"
    #签到历史
    sign_history = apiRequest_get(history_path, app_id,app_Version,Authorization, "")
    #补签
    if resign:
        print("正在尝试补签")
        #补签前的补签卡
        cansign_before = apiRequest_get(can_resign, app_id,app_Version,Authorization, "")
        if cansign_before and cansign_before.get('body'):
            cansign_before_time = cansign_before['body']['Value']
        else:
            cansign_before_time = False
        print(cansign_before_time)
        for i in ['1','2','3','4','5','6','7']:
            if not i>resign:
                print('round ' + str(i))
                resign_time = int(time.time())-86400*i
                r_date, r_time = timeStamp2time(resign_time)
                resign_data = apiRequest_post(resign_path,app_id,app_Version,Authorization,'["' + r_date + 'T15:59:59+0800"]')
                print(resign_data)
            else:
                break
        #补签后的补签卡
        cansign_after = apiRequest_get(can_resign, app_id,app_Version,Authorization, "")
        if cansign_after and cansign_after.get('body'):
            cansign_after_time = cansign_after['body']['Value']
        else:
            cansign_after_time = False
        print(cansign_after_time)
        #使用的补签卡
        if cansign_before_time and cansign_after_time:
            times_resigned = cansign_after_time-cansign_before_time
        else:
            times_resigned = 0
    else:
        times_resigned = False
    #签到
    sign_data = apiRequest_get(sign_path,app_id,app_Version,Authorization, "")
    if sign_data and sign_data.get('body'):
        sign_info = apiRequest_get(is_sign, app_id,app_Version,Authorization, "")
        if sign_data['body']['GetExp']:
            if times_resigned:
                sign_result_post ='补签成功' + str(times_resigned) + '/' + str(resign) +  '天\n签到成功：' + str(sign_info['body']['ContinuousSignDays']) + '天\n好感度：' + str(sign_data['body']['Reward']) + '\n硬币：' + str(sign_data['body']['GetCoin']) + '\n经验值：' + str(sign_data['body']['GetExp']) + '\n签到卡片：' + sign_data['body']['Description'] + sign_data['body']['Name'] + '\n' + sign_data['body']['PictureUrl']
            else:
                sign_result_post = '签到成功：' + str(sign_info['body']['ContinuousSignDays']) + '天\n好感度：' + str(sign_data['body']['Reward']) + '\n硬币：' + str(sign_data['body']['GetCoin']) + '\n经验值：' + str(sign_data['body']['GetExp']) + '\n签到卡片：' + sign_data['body']['Description'] + sign_data['body']['Name'] + '\n' + sign_data['body']['PictureUrl']
            title_post = '兽耳助手签到' + str(sign_info['body']['ContinuousSignDays'])
        else:
            sign_result_post = '今日已签到：' + str(sign_info['body']['ContinuousSignDays']) + '天\n签到卡片：' + sign_data['body']['Description'] + sign_data['body']['Name'] + '\n' + sign_data['body']['PictureUrl']
            title_post = '兽耳助手签到' + str(sign_info['body']['ContinuousSignDays'])
    else:
        sign_result_post = '签到失败'
        title_post = '兽耳助手签到'
    #VIP抽奖
    vip_info_data = apiRequest_get(vip_info,app_id,app_Version,Authorization,"")
    if vip_info_data and vip_info_data.get('body'):
        if vip_info_data['body']['rollNum'] > 0:
            vip_roll_data = apiRequest_post(vip_roll,app_id,app_Version,Authorization,"")
            vip_roll_post = "VIP抽奖成功：" + vip_roll_data['body']['Value']['description']
        else:
            vip_roll_data = "抽奖次数不足"
            if vip_info_data['body']['isValid']:
                vip_roll_post = "今天已经抽过奖了"
            else:
                vip_roll_post = "VIP抽奖失败：您还不是VIP"
    else:
        vip_roll_data = "抽奖次数不足"
        vip_roll_post = "VIP抽奖失败"
    #能量兑换好感度
    energy_info_data = apiRequest_get(energy_info_path + "?code=" + Energy_code,app_id,app_Version,Authorization,"")
    if energy_info_data and energy_info_data.get('body'):
        if energy_info_data['body']['Energy'] > 0:
            energy_reward_data = apiRequest_get(energy_reward_path + "?code=" + Energy_code, app_id,app_Version,Authorization,"")
            energy_reward_post = "能量值：" + str(energy_info_data['body']['Energy']) + "/" +str(energy_info_data['body']['MaxEnergy']) + "\n好感度兑换成功。\n助手：" + servant_name[energy_reward_data['body']['code']] + " LV" + str(energy_reward_data['body']['Level']) +" (" + original_energy_post + "→" + str(energy_reward_data['body']['Favorability']) + "/" + str(energy_info_data['body']['MaxFavorability']) + ")"
        else:
            energy_reward_data = "您的能量值不足，无法兑换"
            energy_reward_post = "能量值：" + str(energy_info_data['body']['Energy']) + "/" +str(energy_info_data['body']['MaxEnergy']) + "\n好感度兑换失败：当前没有能量。\n助手：" + servant_name[energy_info_data['body']['code']] + " LV" + str(energy_info_data['body']['Level']) + " (" + original_energy_post + "→" + str(energy_info_data['body']['Favorability']) + "/" + str(energy_info_data['body']['MaxFavorability']) + ")"
    else:
        energy_reward_data = "您的能量值不足，无法兑换"
        energy_reward_post = "能量兑换失败"
    return sign_data, vip_info_data, vip_roll_data, energy_info_data, energy_reward_data, sign_info, sign_history, sign_result_post, title_post, vip_roll_post, energy_reward_post

try:
    sign_data, vip_info_data, vip_roll_data, energy_info_data, energy_reward_data, sign_info, sign_history, sign_result_post, title_post, vip_roll_post, energy_reward_post = mimikko()
    now_date, now_time = timeStamp2time(time.time()+28800)
    #print(time.time())
    # # sign_data
    print('sign_data', sign_data)
    # # roll info
    print('vip_roll_data', vip_roll_data)
    # # Energy info
    print('energy_info_data', energy_info_data)
    # # Energy reward
    print(energy_reward_data)
    # # sign_info
    # # sign_history
    print(sign_history)
    print('\n' + '\n' + '现在是：' + now_time + '\n' + sign_result_post + '\n' + vip_roll_post + '\n' + energy_reward_post)  
except Exception as e:
    print(e)
try:
    # print(len(sys.argv))
    if SCKEY:
        # print("有SCKEY")
        print("正在推送到微信")
        post_info = "?text=" + title_post + "&desp=<p>" + re.sub('\\n', '  \n', '现在是：' + now_time + '\n' + sign_result_post + '\n' + vip_roll_post + '\n' + energy_reward_post) + "</p>"
        post_data = requests.get(server_api + SCKEY + '.send' + post_info)
        print(post_data)
    else:
        print("没有SCKEY")
except Exception as e:
    print(e)
