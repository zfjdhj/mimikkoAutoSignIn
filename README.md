# mimikkoAutoSignin

本项目使用GitHub Actions，用于兽耳助手定时`每日签到`/`兑换能量`/`VIP每日抽奖`，并可选`推送到微信`

## 使用效果：
![result](/pic/result.png)

## 使用说明

#### 0. 先fork本项目 [![GitHub forks](https://img.shields.io/github/forks/cyb233/mimikkoAutoSignIn?style=social)](https://github.com/cyb233/mimikkoAutoSignIn)

#### 1. 使用抓包软件获取兽耳助手的app_id,Authorization
> - 抓包软件怎么用？请去问百度谷歌 [(只有手机怎么办？→常见的抓包软件)](https://github.com/cyb233/mimikkoAutoSignIn/wiki/%E5%B8%B8%E8%A7%81%E7%9A%84%E6%8A%93%E5%8C%85%E8%BD%AF%E4%BB%B6)
>> - 注意，部分环境下Authorization会失效，如使用同一设备重新进行登录

#### 2. 在设置中创建action secrets `APP_ID`,`AUTHORIZATION`,`ENERGY`;
> - ENERGY用于签到及兑换能量，仅可设置下列code值：

> |code|ServantName|
> |-----|-----|
> |`nonona`|诺诺纳|
> |`momona`|梦梦奈|
> |`ariana`|爱莉安娜|
> |`miruku`|米璐库|
> |`nemuri`|奈姆利|
> |`ruri`|琉璃|
> |`alpha0`|阿尔法零|
> |`miruku2`|米露可|
> |`ulrica`|优莉卡|

> ![三个secrets](/pic/Screenshot_2021_0109_222130.png)

#### 3. 在actions中开启
> - **请勿滥用GitHub Actions！**

#### 4. 修改自动运行时间：
> - 打开`mimikkoAutoSignIn/.github/workflows/auto_sign_in.yml`
> - 在`第12行`修改`cron表达式`，默认北京时间每天`3:30`,`17:30`执行
> - cron表达式怎么改？请去问百度谷歌

#### 5. (可选)使用server酱推送到微信：
> - 在server酱官网 sc.ftqq.com 登录并复制`SCKEY`
> - 在设置中创建action secrets `SCKEY`
> ![推送的secrets](/pic/Screenshot_2021_0109_222138.png)
