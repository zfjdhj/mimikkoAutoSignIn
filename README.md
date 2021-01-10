# mimikkoAutoSignin

用于兽耳助手自动签到

## 使用

0. 先fork本项目

1. 使用抓包软件获取兽耳助手的的app_id,Authorization

2. 在设置中创建action secrets
`APP_ID`,`AUTHORIZATION`,`ENERGY`;
 - ENERGY用于兑换能量，仅取下列code值：
   - code=`nonona`,ServantName=诺诺纳
   - code=`momona`,ServantName=梦梦奈
   - code=`ariana`,ServantName=爱莉安娜
   - code=`miruku`,ServantName=米璐库
   - code=`nemuri`,ServantName=奈姆利
   - code=`ruri`,ServantName=琉璃
   - code=`alpha0`,ServantName=阿尔法零
   - code=`miruku2`,ServantName=米露可
   - code=`ulrica`,ServantName=优莉卡
![secrets1](/pic/Screenshot_2021_0109_222130.png)
3. 在actions中开启

4. (可选)使用server酱推送到微信：
 - 在server酱官网 sc.ftqq.com 登录并复制`SCKEY`
 - 在设置中创建action secrets `SCKEY`
![secrets2](/pic/Screenshot_2021_0109_222138.png)

5. 使用效果：
![result](/pic/Screenshot_2021_0110_090228.png)

