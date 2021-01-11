# mimikkoAutoSignin

用于兽耳助手自动每日签到/兑换能量/VIP每日抽奖，并可选推送到微信

## 使用

0. 先fork本项目 [![GitHub forks](https://img.shields.io/github/forks/cyb233/mimikkoAutoSignIn?style=social)](https://github.com/cyb233/mimikkoAutoSignIn)

1. 使用抓包软件获取兽耳助手的app_id,Authorization
 - 抓包软件怎么用？请去问百度谷歌

2. 在设置中创建action secrets
`APP_ID`,`AUTHORIZATION`,`ENERGY`;
 - ENERGY用于签到及兑换能量，仅可设置下列code值：

|code|ServantName|
|-----|-----|
|`nonona`|诺诺纳|
|`momona`|梦梦奈|
|`ariana`|爱莉安娜|
|`miruku`|米璐库|
|`nemuri`|奈姆利|
|`ruri`|琉璃|
|`alpha0`|阿尔法零|
|`miruku2`|米露可|
|`ulrica`|优莉卡|

![secrets1](/pic/Screenshot_2021_0109_222130.png)

3. 在actions中开启
 - **请勿滥用GitHub Actions！**

4. 修改自动运行时间：
 - 打开`mimikkoAutoSignIn/.github/workflows/auto_sign_in.yml`
 - 在`第12行`修改`cron表达式`，默认北京时间每天`3:30`,`17:30`执行
 - cron表达式怎么改？请去问百度谷歌

5. (可选)使用server酱推送到微信：
 - 在server酱官网 sc.ftqq.com 登录并复制`SCKEY`
 - 在设置中创建action secrets `SCKEY`
![secrets2](/pic/Screenshot_2021_0109_222138.png)

6. 使用效果：
![result1](/pic/Screenshot_2021_0111_040459.png)
![result2](/pic/Screenshot_2021_0111_141226.png)

