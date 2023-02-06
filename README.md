# smpArcbot plugin

## A simple chatbot to query Arcaea song scores
Running on nonebot.  
如果你是一个只想查分的玩家，首先确保安装了python，并且有如下模块：  
`imgkit` 版本`1.2.2`  
`nonebot2` 版本`2.0.0rc2`  
`nonebot-adpter-cqhttp` 版本`2.0.0b1`  
`nonebot-adapter-onebot` 版本`2.1.5`  
（建议直接用conda配置一个新的环境）
首先需要搭建cqhttp，出门右转`https://github.com/Mrs4s/go-cqhttp/releases`，选择`go-cqhttp_windows_amd64.exe`下载，然后执行exe文件，开始配置  

![图片](https://user-images.githubusercontent.com/89081551/216970675-ebe57a3a-17f8-40f6-8ce0-86158b0c4113.png)

选择`3: 反向websockets通信`，配置完成后会出现一个`config.yml`的文件，用记事本打开，将机器人的QQ账号和密码填上，其他就没什么要管的了，如果出现什么问题可以参考官方文档`https://docs.go-cqhttp.org/`，或者直接百度（有很多相关的教程）。  
  
##使用方法（How To Use）  
1、进入smpArcbot目录。右键打开PowerShell终端，输入cmd切换到命令提示行。  
enter /smpArcbot, right click and enter Powershell, input cmd to switch to command console.  
2、使用命令`activate your_environment_here`，激活你已经配置好的python环境，使用命令`python bot.py`开始运行Arcbot脚本。  
use instruction `activate your_environment_here` to activate your python environment. use `python bot.py`to run the bot scripts.  
3、go-cqhttp安装好之后会生成一个`go-cqhttp.bat`的批处理文件，双击执行。当出现:   
double click `go-cqhttp.bat`. when you see:  
![图片](https://user-images.githubusercontent.com/89081551/216973976-e3ce92b0-7b2c-4208-aaa9-ee12e02e02d1.png)
可以确定机器人已经完成连接，同时刚刚的命令提示符窗口会有Onebot插件提示`Connection Open`，现在就可以向你的机器人发送消息了！  
Now you can chat with your bot!  
  
##使用说明（Instruction）  
1、使用`/arc bind [your id]`来绑定你的arcaea id。  
2、使用`/arc songinfo [songid]`来查询某首曲子的信息，如果需要查询定数，使用`/arc songinfo cst [songid]`来查询，注意songid一般是曲子的小写英文名称（去空格），当然你也可以使用曲子的别名进行模糊查询（比如`/arc songinfo cst 世征`，`/arc songinfo cst FTR6`，`/arc songinfo cst 威猛先生`都会被定向到`World Vanquisher`）  
3、使用`/arc lookup [username]`来查看（视奸）别人的id和ptt。（这个功能有些不准确，有待完善）  
4、使用`/arc b30`来获取你的b30和r10曲目，r10的算法是采用`http://wiki.arcaea.cn/%E6%BD%9C%E5%8A%9B%E5%80%BC#ptt.E7.BB.84.E6.88.90`的算法来计算。
