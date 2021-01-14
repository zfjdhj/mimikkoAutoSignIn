# mimikkoAutoSignin

用于兽耳桌面自动签到

## 使用

1. 抓包软件获取签到时的app_id,Authorization

2. 创建action secrets
`secrets.APP_ID`,`secrets.AUTHORIZATION`;
`可选功能`日志输出到文件，需要设定`secrets.SECRET_TOKEN`

3. 修改config.json

``` json


```

## Hoshino插件版

项目地址<https://github.com/zfjdhj/zfjbot-mimikko>

## 说明

这只是一个脚本，不要期望有太多功能。

或者使用大佬的另一版本

<https://github.com/cyb233/mimikkoAutoSignIn>

## 更新

1. 新增日志输出到文件，需要设定secrets.SECRET_TOKEN
**注意：**脚本包含上传功能，已关闭action push触发，如有需要请自行开启（会套娃），测试完毕后尽快关闭

2. 新增config.json用于设定助手

3. 感谢cyb233大佬提供的建议
