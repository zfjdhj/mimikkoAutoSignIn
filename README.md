# mimikkoAutoSignin

本项目使用GitHub Actions，用于[兽耳助手](https://www.mimikko.cn/)定时`每日签到/补签`/`兑换能量`/`VIP每日抽奖`，并可选`推送到微信`  
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/cyb233/mimikkoAutoSignIn/CI)](https://github.com/cyb233/mimikkoAutoSignIn/actions)
>[keylol帖子](https://keylol.com/t675496-1-1)
## 使用效果：
![result](/pic/result.png)

## 使用说明 
> 熟悉GitHub相关操作的，可以直接看下面，不熟悉的话，可以去看由[@Amcc1860](https://github.com/Amcc1860)编写的[保姆级教程](https://github.com/cyb233/mimikkoAutoSignIn/issues/4)
<details markdown='1'><summary>点击查看使用说明</summary>

#### 0. 先fork本项目（本项目已fork人数 [![GitHub forks](https://img.shields.io/github/forks/cyb233/mimikkoAutoSignIn?style=social)](https://github.com/cyb233/mimikkoAutoSignIn)）
> 打开[本项目](https://github.com/cyb233/mimikkoAutoSignIn)，并点击如图fork按钮
> ![fork](/pic/fork.png)

#### 1. 使用抓包软件获取兽耳助手的app_id,Authorization等数据
> - 抓包软件怎么用？请去问百度谷歌 [(只有手机怎么办？→常见的抓包软件)](https://github.com/cyb233/mimikkoAutoSignIn/wiki/%E5%B8%B8%E8%A7%81%E7%9A%84%E6%8A%93%E5%8C%85%E8%BD%AF%E4%BB%B6)
>> - 注意，部分环境下Authorization会失效，如使用同一设备重新进行登录
>>> ~~如果想避免这种情况可以抓取登录id和password~~ 账号登录功能没搞定，暂时放弃

#### 2. 在设置中创建action secrets：
> |secret名称|是否必要|说明|
> |-----|-----|-----|
> |`APP_ID`|√|APP_ID，通过抓包获取|
> |`AUTHORIZATION`|√|验证账号用，通过抓包获取|
> |`ENERGY`|x|详见下个表格|
> |`RESIGN`|x|当设置为1~7后每天会尝试向前补签对应天数|
> |`SCKEY`|x|微信推送，详见步骤5|
> - ENERGY参数用于签到及兑换能量，使用的code值为助手代码，下表是已知的code值
> - 注意：本项目不检查code可用性，如出现新助手而本表未更新，可自行抓取code值；由于随意输入错误助手code所可能导致的问题，本项目不负任何责任

> |code|ServantName|
> |-----|-----|
> |留空/不填|缺省值：梦梦奈|
> |`nonona`|诺诺纳|
> |`momona`|梦梦奈|
> |`ariana`|爱莉安娜|
> |`miruku`|米璐库|
> |`nemuri`|奈姆利|
> |`ruri`|琉璃|
> |`alpha0`|阿尔法零|
> |`miruku2`|米露可|
> |`ulrica`|优莉卡|

> 如图`setting`→`secrets→new repository secret`
> ![secrets](/pic/secrets.png)

#### 3. 在actions中开启
> - **请勿滥用GitHub Actions！**  
> - 如图点击`I understand my workflows, go ahead and enable them`，并手动执行一次
> ![actions](/pic/actions.jpg)
> ![run](https://user-images.githubusercontent.com/35195193/104328725-13405200-5527-11eb-8540-c804a6d1142e.png)

#### 4. 修改自动运行时间：
> - 打开`mimikkoAutoSignIn/.github/workflows/auto_sign_in.yml`
> - 在`第12行`修改`cron表达式`，默认北京时间每天`3:30`,`17:30`执行
> - cron表达式怎么改？请去问百度谷歌

#### 5. (可选)使用server酱推送到微信：
> - 在server酱官网 sc.ftqq.com 登录并复制`SCKEY`
> - 在设置中创建action secrets `SCKEY`
> ![推送的secrets](/pic/Screenshot_2021_0109_222138.png)
</details>
  
  
## 用前预知
使用本项目前，您已知悉以下内容：
- 本项目完全开源，使用时如有任何不放心请自行检阅代码（或提issues也行）
- 本项目使用的Secrets均保存于GitHub服务器中，且一旦保存，即使是用户自己也无法再次查看
- 本项目均使用GitHub Actions定时运行，理论上可以下载并本地定时运行，但我没试过
- 使用本项目请遵循兽耳助手《用户服务协议》，请勿使用本项目进行任何违法行为
- 本项目不对任何不可抗力负责，包括但不限于 罢工，自然和人为灾害，战争，网络攻击，拿服务器CPU烧烤，第三次世界大战，G胖数3，圣杯战争导致的煤气爆炸，没交网费，二哈拆房，生化危机，总是单身，异形入侵，考试挂科，三体来袭 等各种软件服务协议会写的东西
  
  
## 闲着没事上班摸鱼一小时算出来的数据
<details markdown='1'><summary>展开看图</summary>

![兽耳助手签到所需时长](pic/mimikko_sign.png)
</details>
