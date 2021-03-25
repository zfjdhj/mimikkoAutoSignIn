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
import hashlib
import hmac
import base64
import urllib.parse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'e:l:a:u:p:s:r:d:c:')
    print('正在获取secret参数')
    for o, a in optlist:
        if o == '-e' and a.strip() != '':
            Energy_code = a.strip()
            print("Energy_code存在")
        elif o == '-e':
            Energy_code = 'momona'
            print("Energy_code不存在，默认'momona'")
        if o == '-a' and a.strip() != '':
            Authorization = a.strip()
            print("Authorization存在")
        elif o == '-a':
            Authorization = False
            print("Authorization不存在")
        if o == '-u' and a.strip() != '':
            user_id = a.strip()
            print("user_id存在")
        elif o == '-u':
            user_id = False
            print("user_id不存在")
        if o == '-p' and a.strip() != '':
            user_password = a.strip()
            print("user_password存在")
        elif o == '-p':
            user_password = False
            print("user_password不存在")
        if o == '-s' and a.strip() != '':
            SCKEY = a.strip()
            print("SCKEY存在")
        elif o == '-s':
            SCKEY = False
            print("SCKEY不存在")
        if o == '-d' and a.strip() != '':
            DDTOKEN = a.strip()
            print("DDTOKEN存在")
        elif o == '-d':
            DDTOKEN = False
            print("DDTOKEN不存在")
        if o == '-c' and a.strip() != '':
            DDSECRET = a.strip()
            print("DDSECRET存在")
        elif o == '-c':
            DDSECRET = False
            print("DDSECRET不存在")
        if o == '-r':
            if a.strip() in ['1', '2', '3', '4', '5', '6', '7']:
                resign = a.strip()
                print("resign开启")
            else:
                resign = False
                print("resign关闭")
        if o == '-l':
            if a.strip().upper() == 'FALSE':
                login = False
                print("login关闭")
            else:
                login = True
                print("login开启")
    if Authorization and user_id and user_password and login and Energy_code and resign and SCKEY and DDTOKEN and DDSECRET:
        print('获取参数结束')
    else:
        print('获取参数结束')
except Exception as e:
    print('获取参数错误：', e)
    sys.exit(1)

login_path = 'https://api1.mimikko.cn/client/user/LoginWithPayload' # 登录(post)
is_sign = 'https://api1.mimikko.cn/client/user/GetUserSignedInformation' # 今天是否签到
history_path = 'https://api1.mimikko.cn/client/dailysignin/log/30/0' # 签到历史
can_resign = 'https://api1.mimikko.cn/client/love/getcanresigntimes' # 补签卡数量
defeat_set = 'https://api1.mimikko.cn/client/Servant/SetDefaultServant' # 设置默认助手
resign_path = 'https://api1.mimikko.cn/client/love/resign?servantId=' # 补签(post)
sign_path = 'https://api1.mimikko.cn/client/RewardRuleInfo/SignAndSignInformationV3' # 签到
energy_info_path = 'https://api1.mimikko.cn/client/love/GetUserServantInstance' # 获取助手状态
energy_reward_path = 'https://api1.mimikko.cn/client/love/ExchangeReward' # 兑换助手能量
vip_info = 'https://api1.mimikko.cn/client/user/GetUserVipInfo' # 获取会员状态
vip_roll = 'https://api1.mimikko.cn/client/roll/RollReward' # 会员抽奖(post)
sc_api = 'https://sc.ftqq.com/' # 微信推送
sct_api = 'https://sctapi.ftqq.com/' # 微信推送
ding_api = 'https://oapi.dingtalk.com/robot/send?' # 钉钉推送
app_Version = '3.1.6'
app_id = 'wjB7LOP2sYkaMGLC'
servant_name = {'nonona':'诺诺纳', 'momona':'梦梦奈', 'ariana':'爱莉安娜', 'miruku':'米璐库', 'nemuri':'奈姆利', 'ruri':'琉璃', 'alpha0':'阿尔法零', 'miruku2':'米露可', 'ulrica':'优莉卡', 'giwa':'羲和', 'maya':'摩耶'}
# 登录post
def loginRequest_post(url, app_id, app_Version, params):
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
        with requests.post(url, headers=headers_post, data=params_post, verify=False, timeout=300) as resp:
            res = resp.json()
            return res
    except Exception as ex:
        print(ex)
# get请求
def apiRequest_get(url, app_id, app_Version, Authorization, params):
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
# post请求
def apiRequest_post(url, app_id, app_Version, Authorization, params):
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
        with requests.post(url, headers=headers_post, data=params_post, verify=False, timeout=300) as resp:
            res = resp.json()
            return res
    except Exception as ex:
        print(ex)
# 时间格式化
def timeStamp2time(timeStamp):
    timeArray = time.localtime(timeStamp)
    firstStyleTime = time.strftime('%Y-%m-%d', timeArray)
    secondStyleTime = time.strftime('%Y年%m月%d日 %H:%M:%S', timeArray)
    return firstStyleTime, secondStyleTime
# 钉钉post
def ddpost(ding_api, DDTOKEN, DDSECRET, title_post, post_text):
    timestamp = str(round(time.time() * 1000))
    secret_enc = DDSECRET.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, DDSECRET)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    headers_post = {
        'Content-Type': 'application/json',
    }
    url = ding_api + 'access_token=' + DDTOKEN + '&timestamp=' + timestamp + '&sign=' + sign
    post_info = '{"msgtype":"markdown","markdown":{"title":"' + title_post + '", "text":"' + post_text + '"}}'
    print(post_info)
    post_data = requests.post(url, headers=headers_post, json=json.loads(post_info))
    return post_data.text
# server酱post
def scpost(sc_api, SCKEY, title_post, post_text):
    headers_post = {
        'Content-Type': 'application/json',
    }
    post_info = '{"text":"' + title_post + '","desp":"' + post_text + '"}'
    url = sc_api + SCKEY + '.send'
    post_data = requests.post(url, headers=headers_post, json=json.loads(post_info))
    return post_data.text

def mimikko():
    global Authorization
    #登录
    print('开始登录')
    if login and user_id and user_password:
        print("使用ID密码登录")
        user_password_sha = hashlib.sha256(user_password.encode('utf-8')).hexdigest()
        login_data = loginRequest_post(login_path, app_id, app_Version, '{"password":"' + user_password_sha + '", "id":"' + user_id + '"}')
        if login_data and login_data.get('body'):
            Authorization = login_data['body']['Token']
            print("登录成功！")
        else:
            if Authorization:
                print("登录错误，尝试使用保存的Authorization")
            else:
                if SCKEY:
                    print("登录错误，正在推送到微信")
                    post_data_a = scpost(sc_api, SCKEY, "兽耳助手签到登录错误", "登录错误，且未找到Authorization，请访问GitHub检查")
                    print(post_data_a)
                    #post_data_b = scpost(sct_api, SCKEY, "兽耳助手签到登录错误", "登录错误，且未找到Authorization，请访问GitHub检查")
                    #print(post_data_b)
                if DDTOKEN and DDSECRET:
                    post_data = ddpost(ding_api, DDTOKEN, DDSECRET, "兽耳助手签到登录错误", "登录错误，且未找到Authorization，请访问GitHub检查")
                    print(post_data)
                sys.exit('登录错误，且未找到Authorization！！！')
    elif login:
        if Authorization:
            print("未找到登录ID或密码，尝试使用保存的Authorization")
        else:
            if SCKEY:
                print("登录错误，正在推送到微信")
                post_data_a = scpost(sc_api, SCKEY, "兽耳助手签到登录错误", "登录错误，未找到登录ID、密码或Authorization，请访问GitHub检查")
                print(post_data_a)
                #post_data_b = scpost(sct_api, SCKEY, "兽耳助手签到登录错误", "登录错误，未找到登录ID、密码或Authorization，请访问GitHub检查")
                #print(post_data_b)
            if DDTOKEN and DDSECRET:
                print("登录错误，正在推送到钉钉")
                post_data = ddpost(ding_api, DDTOKEN, DDSECRET, "兽耳助手签到登录错误", "登录错误，未找到登录ID、密码或Authorization，请访问GitHub检查")
                print(post_data)
            sys.exit('请在Secret中保存登录ID和密码或Authorization！！！')
    else:
        if Authorization:
            print("使用Authorization验证")
        else:
            if SCKEY:
                print("登录错误，正在推送到微信")
                post_data_a = scpost(sc_api, SCKEY, "兽耳助手签到登录错误", "登录错误，未找到Authorization，请访问GitHub检查")
                print(post_data_a)
                #post_data_b = scpost(sct_api, SCKEY, "兽耳助手签到登录错误", "登录错误，未找到Authorization，请访问GitHub检查")
                #print(post_data_b)
            if DDTOKEN and DDSECRET:
                post_data = ddpost(ding_api, DDTOKEN, DDSECRET, "兽耳助手签到登录错误", "登录错误，未找到Authorization，请访问GitHub检查")
                print(post_data)
            sys.exit('请在Secret中保存登录ID和密码或Authorization！！！')
    #设置默认助手
    print('设置默认助手')
    defeat_data = apiRequest_get(defeat_set + "?code=" + Energy_code, app_id, app_Version, Authorization, "")
    #执行前的好感度
    original_energy_data = apiRequest_get(energy_info_path + "?code=" + Energy_code, app_id, app_Version, Authorization, "")
    if original_energy_data and original_energy_data.get('body'):
        original_energy_post = str(original_energy_data['body']['Favorability'])
    else:
        energy_reward_post = "*"
    #签到历史
    sign_history = apiRequest_get(history_path, app_id, app_Version, Authorization, "")
    #补签
    if resign:
        print("正在尝试补签")
        #补签前的补签卡
        cansign_before = apiRequest_get(can_resign, app_id, app_Version, Authorization, "")
        if cansign_before and cansign_before.get('body'):
            cansign_before_time = cansign_before['body']['Value']
        else:
            cansign_before_time = False
        print(cansign_before_time)
        for i in ['1', '2', '3', '4', '5', '6', '7']:
            if not i>resign:
                print('round ' + str(i))
                resign_time = int(time.time())-86400*int(i)
                r_date, r_time = timeStamp2time(resign_time)
                resign_data = apiRequest_post(resign_path, app_id, app_Version, Authorization, '["' + r_date + 'T15:59:59+0800"]')
                print(resign_data)
            else:
                break
        #补签后的补签卡
        cansign_after = apiRequest_get(can_resign, app_id, app_Version, Authorization, "")
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
    print('正在尝试签到')
    sign_data = apiRequest_get(sign_path, app_id, app_Version, Authorization, "")
    if sign_data and sign_data.get('body'):
        sign_info = apiRequest_get(is_sign, app_id, app_Version, Authorization, "")
        if sign_data['body']['GetExp']:
            if times_resigned:
                sign_result_post ='补签成功' + str(times_resigned) + '/' + str(resign) +  '天\n签到成功：' + str(sign_info['body']['ContinuousSignDays']) + '天\n好感度：' + str(sign_data['body']['Reward']) + '\n硬币：' + str(sign_data['body']['GetCoin']) + '\n经验值：' + str(sign_data['body']['GetExp']) + '\n签到卡片：' + sign_data['body']['Description'] + sign_data['body']['Name'] + '\n' + sign_data['body']['PictureUrl']
            else:
                sign_result_post = '签到成功：' + str(sign_info['body']['ContinuousSignDays']) + '天\n好感度：' + str(sign_data['body']['Reward']) + '\n硬币：' + str(sign_data['body']['GetCoin']) + '\n经验值：' + str(sign_data['body']['GetExp']) + '\n签到卡片：' + sign_data['body']['Description'] + sign_data['body']['Name'] + '\n' + sign_data['body']['PictureUrl']
            title_ahead = '兽耳助手签到' + str(sign_info['body']['ContinuousSignDays'])
        else:
            sign_result_post = '今日已签到：' + str(sign_info['body']['ContinuousSignDays']) + '天\n签到卡片：' + sign_data['body']['Description'] + sign_data['body']['Name'] + '\n' + sign_data['body']['PictureUrl']
            title_ahead = '兽耳助手签到' + str(sign_info['body']['ContinuousSignDays'])
    else:
        sign_result_post = '签到失败'
        title_ahead = '兽耳助手签到'
    #VIP抽奖
    print('正在尝试VIP抽奖')
    vip_info_data = apiRequest_get(vip_info, app_id, app_Version, Authorization, "")
    if vip_info_data and vip_info_data.get('body'):
        if vip_info_data['body']['rollNum'] > 0:
            vip_roll_data = apiRequest_post(vip_roll, app_id, app_Version, Authorization, "")
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
    print('正在尝试兑换能量')
    energy_info_data = apiRequest_get(energy_info_path + "?code=" + Energy_code, app_id, app_Version, Authorization, "")
    if energy_info_data and energy_info_data.get('body'):
        if energy_info_data['body']['Energy'] > 0:
            energy_reward_data = apiRequest_get(energy_reward_path + "?code=" + Energy_code, app_id, app_Version, Authorization, "")
            title_post = title_ahead + servant_name[energy_reward_data['body']['code']] + "好感度" + str(energy_reward_data['body']['Favorability'])
            energy_reward_post = "能量值：" + str(energy_info_data['body']['Energy']) + "/" +str(energy_info_data['body']['MaxEnergy']) + "\n好感度兑换成功\n助手：" + servant_name[energy_reward_data['body']['code']] + " LV" + str(energy_reward_data['body']['Level']) +" (" + original_energy_post + "→" + str(energy_reward_data['body']['Favorability']) + "/" + str(energy_info_data['body']['MaxFavorability']) + ")"
        else:
            energy_reward_data = "您的能量值不足，无法兑换"
            title_post = title_ahead + servant_name[energy_info_data['body']['code']] + "好感度" + str(energy_info_data['body']['Favorability'])
            energy_reward_post = "能量值：" + str(energy_info_data['body']['Energy']) + "/" +str(energy_info_data['body']['MaxEnergy']) + "\n好感度兑换失败：当前没有能量\n助手：" + servant_name[energy_info_data['body']['code']] + " LV" + str(energy_info_data['body']['Level']) + " (" + original_energy_post + "→" + str(energy_info_data['body']['Favorability']) + "/" + str(energy_info_data['body']['MaxFavorability']) + ")"
    else:
        energy_reward_data = "您的能量值不足，无法兑换"
        title_post = title_ahead
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
except Exception as em:
    print('mimikko', em)

try:
    # print(len(sys.argv))
    if SCKEY:
        # print("有SCKEY")
        if title_post and now_time and sign_result_post and vip_roll_post and energy_reward_post:
            print("运行成功，正在推送到微信")
            post_text = "<p>" + re.sub('\\n', '  \n', '现在是：' + now_time + '\n' + sign_result_post + '\n' + vip_roll_post + '\n' + energy_reward_post) +"</p>"
            post_data_a = scpost(sc_api, SCKEY, title_post, post_text)
            print('server酱', post_data_a)
            #post_data_b = scpost(sct_api, SCKEY, title_post, post_text)
            #print('server酱Turbo版', post_data_b)
    else:
        print("运行成功，没有SCKEY")
except Exception as es:
    if SCKEY:
        print("数据异常，正在推送到微信")
        post_data_a = scpost(sc_api, SCKEY, "兽耳助手签到数据异常", "兽耳助手签到数据异常，请访问GitHub检查")
        print('server酱', post_data_a)
        #post_data_b = scpost(sct_api, SCKEY, "兽耳助手签到数据异常", "兽耳助手签到数据异常，请访问GitHub检查")
        #print('server酱Turbo版', post_data_b)
    else:
        print("数据异常，且没有SCKEY，未推送")
    print('sc', es)
try:
    # print(len(sys.argv))
    if DDTOKEN and DDSECRET:
        #print("有DDTOKEN和DDSECRET")
        if title_post and now_time and sign_result_post and vip_roll_post and energy_reward_post:
            print("运行成功，正在推送到钉钉")
            post_text = "<p>" + re.sub('\\n', '  \n', '现在是：' + now_time + '\n' + sign_result_post + '\n' + vip_roll_post + '\n' + energy_reward_post) +"</p>"
            post_data = ddpost(ding_api, DDTOKEN, DDSECRET, title_post, post_text)
            print('钉钉', post_data)
    else:
        print("运行成功，没有DDTOKEN或DDSECRET")
except Exception as ed:
    if DDTOKEN and DDSECRET:
        print("数据异常，正在推送到钉钉")
        post_data = ddpost(ding_api, DDTOKEN, DDSECRET, "兽耳助手签到数据异常", "兽耳助手签到数据异常，请访问GitHub检查")
        print('钉钉', post_data)
    else:
        print("数据异常，且没有DDTOKEN或DDSECRET，未推送")
    print('dd', ed)
