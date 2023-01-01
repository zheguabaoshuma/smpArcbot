import asyncio.exceptions
import json
from ..Matcher import arc
from nonebot.typing import T_State
from nonebot import logger
import websockets
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import MessageSegment,Message
from io import BytesIO
import imgkit
import brotli

with open('ArcaeaSongDatabase-main/arcsong.json','r',encoding='utf-8') as f1:
    db=json.load(f1)
with open('qq_id2arc_id.txt','r+',encoding='utf-8') as f2:
    rawdata:str=f2.read()
    tempdata=rawdata.splitlines()
    logger.info(tempdata)
    user_dict:dict={}
    try:
        for items in tempdata:
            items=items.split(" ")
            user_dict[items[0]]=items[1]
    except IndexError:
        user_dict
    logger.info(user_dict)


async def songinfo_handler(state:T_State):

    #checker
    if(state['_argv'][0]!='songinfo'):
        return

    songname:str=""
    songinfo:str=""
    #logger.info(state)

    for num in range (1,5):
        try:
            if state['_argv'][1]!='cst' or num!=1:
                songname+=state['_argv'][num]
        except:
            songname=songname.rstrip()
            break
    rawsongname=songname
    songname=songname.lower()
    logger.info(songname)
    if songname =='':
        await arc.finish('请输入歌曲信息')
        return

    for items in db['content']['songs']:
        if items['song_id'] == songname or rawsongname in items['alias']:
            songname=items['song_id']
            songinfo+=("曲名："+items['difficulties'][0]['name_en']+'\n')+\
                      ("曲师： "+items['difficulties'][0]['artist']+"\n"+"bpm: "+str(items['difficulties'][0]['bpm'])+" 难度：")
            if items['difficulties'][0]['difficulty']%2==0:
                songinfo+=str(int(items['difficulties'][0]['difficulty']/2))+" "
            else:
                songinfo += str(int(items['difficulties'][0]['difficulty'] / 2)) + "+ "

            if items['difficulties'][1]['difficulty'] % 2 == 0:
                songinfo+=str(int(items['difficulties'][1]['difficulty']/2))+" "
            else:
                songinfo += str(int(items['difficulties'][1]['difficulty'] / 2)) + "+ "

            if items['difficulties'][2]['difficulty'] % 2 == 0:
                songinfo+=str(int(items['difficulties'][2]['difficulty']/2))+" "
            else:
                songinfo += str(int(items['difficulties'][2]['difficulty'] / 2)) + "+ "

            try:
                if items['difficulties'][3]['difficulty'] % 2 == 0:
                    songinfo += str(int(items['difficulties'][3]['difficulty'] / 2)) + " "
                else:
                    songinfo += str(int(items['difficulties'][3]['difficulty'] / 2)) + "+ "
            except IndexError:
                songinfo
            try:
                nick=""
                for name in items['alias']:
                    nick+=(name+" ")
                songinfo+=("\n"+nick)
            except:songinfo
            break

    if songinfo=="":
        await arc.finish('查询失败~是不是打错id了呢？', at_sender=True)
        return
    try:
        dir:str='c:/Users/Tuuuu/arcbotv2/gamedata/assets/songs/'+songname+'/base.jpg'
        with open(dir,'rb') as imagefile:
            bytesimage=BytesIO(imagefile.read())
            #await arc.send(MessageSegment.image(bytesimage))
    except:
        dir:str='c:/Users/Tuuuu/arcbotv2/gamedata/assets/songs/dl_'+songname+'/base.jpg'
        with open(dir,'rb') as imagefile:
            bytesimage=BytesIO(imagefile.read())
            #await arc.send(MessageSegment.image(bytesimage))

    try:
        if state['_argv'][1]=='cst':
            data: list = []
            async with websockets.connect(uri="wss://arc.estertion.win:616",user_agent_header={'Host': 'arc.estertion.win:616',\
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',\
            'Accept': '*/*',\
            'Accept-Language': 'zh-CN,zh-HK;q=0.8,zh;q=0.7,zh-TW;q=0.5,en-US;q=0.3,en;q=0.2',\
            'Accept-Encoding': 'gzip, deflate, br',\
            'Sec-WebSocket-Version': '13',\
            'Origin': 'https://redive.estertion.win',\
            'Sec-WebSocket-Extensions': 'permessage-deflate',\
            'Sec-WebSocket-Key': 'RybTU78s6vitAlD86nIZfw==',\
            'DNT': '1',\
            'Connection': 'keep-alive, Upgrade',\
            'Sec-Fetch-Dest': 'websocket',\
            'Sec-Fetch-Mode': 'websocket',\
            'Sec-Fetch-Site': 'same-site',\
            'Pragma': 'no-cache',\
            'Cache-Control': 'no-cache',\
            'Upgrade': 'websocket'}) as ws:
                await ws.send('constants')
                for i in range(0,3):
                    temp=await ws.recv()
                    #logger.info(temp)
                    data.append(brotli.decompress(bytes(temp)).decode('utf-8'))
                    #logger.info(data)
                mdata=[]
                for items in data:
                    mdata.append(json.loads(items))
            constantsinfo:dict=mdata[2]['data']
            songinfo+='\n定数: '+str(constantsinfo[songname][0]['constant'])+' '+ \
                      str(constantsinfo[songname][1]['constant']) + ' ' + \
                      str(constantsinfo[songname][2]['constant']) + ' '
            try:
                songinfo+=str(constantsinfo[songname][3]['constant'])
            except IndexError: songinfo
    except:songinfo


    await arc.finish(Message('SongInfo 查询结果\n' + songinfo)+MessageSegment.image(bytesimage), at_sender=True)
    return

async def bind_handler(event:Event,state:T_State):

    #check
    if state['_argv'][0]!='bind':
        return
    user_qqid:str=event.get_user_id()
    user_arcid:str=state['_argv'][1]
    try:
        arc_id=user_dict[user_qqid]
        if arc_id!=user_arcid:
            user_dict[user_qqid]=user_arcid
            for keys in user_dict:
                cookeddata: str = ''
                cookeddata += (keys + ' ' + user_dict[keys] + '\n')
            with open('qq_id2arc_id.txt', 'r+', encoding='utf-8') as f2:
                f2.seek(0)
                f2.write(cookeddata)
            await arc.finish('用户信息更新成功')
        await arc.finish('已经绑定啦！')
    except KeyError:
        user_dict[user_qqid]=user_arcid
        for keys in user_dict:
            cookeddata: str = ''
            cookeddata += (keys + ' ' + user_dict[keys] + '\n')
        with open('qq_id2arc_id.txt', 'r+', encoding='utf-8') as f2:
            f2.seek(0)
            f2.write(cookeddata)
        await arc.finish('用户绑定成功')


def rating(d:dict)->float:
    return d['data'][0]['rating']
def time(d:dict)->float:
    return d['data'][0]['time_played']

async def b30r10_handler(event:Event,state:T_State):

    #checker
    if state['_argv'][0]!='b30':
        return

    userarcid=user_dict[event.get_user_id()]
    await arc.send('稍等一下哦，等待esterTion服务器返回数据。')
    await arc.send('要是我太长时间没响应就重发一次试试,或者去戳戳维护者1139614211')
    recv:str=''
    async with websockets.connect(uri="wss://arc.estertion.win:616",user_agent_header={'Host': 'arc.estertion.win:616',\
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',\
    'Accept': '*/*',\
    'Accept-Language': 'zh-CN,zh-HK;q=0.8,zh;q=0.7,zh-TW;q=0.5,en-US;q=0.3,en;q=0.2',\
    'Accept-Encoding': 'gzip, deflate, br',\
    'Sec-WebSocket-Version': '13',\
    'Origin': 'https://redive.estertion.win',\
    'Sec-WebSocket-Extensions': 'permessage-deflate',\
    'Sec-WebSocket-Key': 'RybTU78s6vitAlD86nIZfw==',\
    'DNT': '1',\
    'Connection': 'keep-alive, Upgrade',\
    'Sec-Fetch-Dest': 'websocket',\
    'Sec-Fetch-Mode': 'websocket',\
    'Sec-Fetch-Site': 'same-site',\
    'Pragma': 'no-cache',\
    'Cache-Control': 'no-cache',\
    'Upgrade': 'websocket'}) as ws:
        await ws.send(userarcid+" 9 12")
        data:list=[]
        while True:
            temp=await ws.recv()
            #logger.info(temp)
            if(temp=='bye'):
                break
            if temp=='queued' or temp=='queried':
                continue
            #logger.info(type(temp))
            data.append(brotli.decompress(bytes(temp)).decode('utf-8'))
        realdata=[]
        for items in data:
            realdata.append(json.loads(items))
        databyrating:list=realdata[3:]
        databytime:list=realdata[3:]
        databyrating.sort(key=rating,reverse=True)
        databytime.sort(key=time,reverse=True)
        b30data=databyrating[0:30]
        r30data:list=databytime[0:30]
        r30data.sort(key=rating,reverse=True)
        r10data=r30data[0:10]
        idnamedict:dict=realdata[0]['data']
        userinfo:dict=realdata[2]['data']
        #logger.info(userinfo)
        #logger.info(idnamedict)
        with open('b30r10picsrc.html','r+') as picf:
            picsrc:str=picf.read()
        counter=1
        total_b30rating:float=0
        for items in b30data:
            mkey='b'+str(counter)+' '
            songid:str=items['data'][0]['song_id']
            songname:str=idnamedict[songid]['en']
            #logger.info(songname)
            score:int=items['data'][0]['score']
            mrating:float=items['data'][0]['rating']
            total_b30rating+=mrating
            constant:float=items['data'][0]['constant']
            diff:int=items['data'][0]['difficulty']
            picsrc=picsrc.replace(mkey,songname,1)
            picsrc=picsrc.replace('Score: ','Score:'+str(score),1)
            #logger.info(score)
            picsrc=picsrc.replace('Rating: ','Rating:'+str(round(mrating,2)),1)
            picsrc=picsrc.replace('Cst: ','Cst:'+str(constant),1)
            if diff==0:
                picsrc=picsrc.replace('diffhere','pst',1)
            elif diff==1:
                picsrc=picsrc.replace('diffhere','prs',1)
            elif diff==2:
                picsrc=picsrc.replace('diffhere','ftr',1)
            elif diff==3:
                picsrc=picsrc.replace('diffhere','byd',1)
            try:
                with open('gamedata/assets/songs/'+songid+'/base_256.jpg','r') as p:
                    picsrc=picsrc.replace('arcahv', songid,1)
                p.close()
            except:
                picsrc=picsrc.replace('arcahv','dl_'+songid,1)
            counter+=1

        counter=1
        total_r10rating:float=0
        for items in r10data:
            mkey='r'+str(counter)+' '
            songid:str=items['data'][0]['song_id']
            songname:str=idnamedict[songid]['en']
            score:int=items['data'][0]['score']
            mrating:float=items['data'][0]['rating']
            total_r10rating+=mrating
            constant:float=items['data'][0]['constant']
            diff:int=items['data'][0]['difficulty']
            picsrc=picsrc.replace(mkey,songname,1)
            picsrc=picsrc.replace('Score: ','Score:'+str(score),1)
            picsrc=picsrc.replace('Rating: ','Rating:'+str(round(mrating,2)),1)
            picsrc=picsrc.replace('Cst: ','Cst:'+str(constant),1)
            if diff==0:
                picsrc=picsrc.replace('diffhere','pst',1)
            elif diff==1:
                picsrc=picsrc.replace('diffhere','prs',1)
            elif diff==2:
                picsrc=picsrc.replace('diffhere','ftr',1)
            elif diff==3:
                picsrc=picsrc.replace('diffhere','byd',1)
            try:
                with open('gamedata/assets/songs/'+songid+'/base_256.jpg') as p:
                    picsrc=picsrc.replace('arcahv', songid,1)
                p.close()
            except:
                picsrc=picsrc.replace('arcahv','dl_'+songid,1)
            counter+=1
        #logger.info(realdata)
        user_id:str=userinfo['user_code']
        user_ptt:float=userinfo['rating']/100
        user_name:str=userinfo['name']
        user_char:int=userinfo['character']
        user_char_uncapped:bool=userinfo['is_char_uncapped']
        picsrc=picsrc.replace('User_Id','UID:'+user_id,1)
        picsrc=picsrc.replace('User_Name',user_name,1)
        picsrc=picsrc.replace('User_Ptt','User_Ptt:'+str(user_ptt),1)
        picsrc=picsrc.replace('apttx',str(round(total_b30rating/30,2)),1)
        picsrc=picsrc.replace('apttx',str(round(total_r10rating/10,2)),1)
        char_dir=''
        charbig_dir=''
        if user_char_uncapped:
            char_dir:str='gamedata/assets/char/'+str(user_char)+'u_icon.png'
            charbig_dir:str='gamedata/assets/char/'+str(user_char)+'u.png'
        else:
            char_dir:str='gamedata/assets/char/'+str(user_char)+'_icon.png'
            charbig_dir:str='gamedata/assets/char/'+str(user_char)+'.png'
        picsrc=picsrc.replace('gamedata/assets/char/1u_icon.png',char_dir,1)
        picsrc=picsrc.replace('gamedata/assets/char/1u.png',charbig_dir,1)
        with open('src.html','w',encoding='utf-8') as s:#使用utf-8编码可以让特殊符号也写进html文件
            s.write(picsrc)
            #logger.info(picsrc)
        s.close()

        kitpath:str='html2img_kit/wkhtmltopdf/bin/wkhtmltoimage.exe'
        cfg=imgkit.config(wkhtmltoimage=kitpath)
        opt = {'enable-local-file-access': None,'zoom':4,'width':2832*2,'height':7296*2}
        imgkit.from_file(r'./src.html','src.jpg',config=cfg,options=opt)

        with open('src.jpg','rb') as brimagefile:
            bytesbrimage=BytesIO(brimagefile.read())
        brimagefile.close()
        await arc.finish(MessageSegment.image(bytesbrimage))


async def lookuphandler(state:T_State):
    #checker
    if state['_argv'][0]!='lookup':
        return

    snd_msg:str=''
    queryid:str=state['_argv'][1]
    async with websockets.connect(uri="wss://arc.estertion.win:616",user_agent_header={'Host': 'arc.estertion.win:616',\
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',\
    'Accept': '*/*',\
    'Accept-Language': 'zh-CN,zh-HK;q=0.8,zh;q=0.7,zh-TW;q=0.5,en-US;q=0.3,en;q=0.2',\
    'Accept-Encoding': 'gzip, deflate, br',\
    'Sec-WebSocket-Version': '13',\
    'Origin': 'https://redive.estertion.win',\
    'Sec-WebSocket-Extensions': 'permessage-deflate',\
    'Sec-WebSocket-Key': 'RybTU78s6vitAlD86nIZfw==',\
    'DNT': '1',\
    'Connection': 'keep-alive, Upgrade',\
    'Sec-Fetch-Dest': 'websocket',\
    'Sec-Fetch-Mode': 'websocket',\
    'Sec-Fetch-Site': 'same-site',\
    'Pragma': 'no-cache',\
    'Cache-Control': 'no-cache',\
    'Upgrade': 'websocket'}) as ws:
        await ws.send('lookup '+ queryid)
        data=await ws.recv()
        try:
            mdata=json.loads(brotli.decompress(data).decode('utf-8'))
        except brotli.brotli.Error:
            await arc.finish('名字是不是打错了呢')
            return
        except asyncio.exceptions.TimeoutError:
            await arc.finish('服务器炸了，等会再试一次吧')

        snd_msg+=queryid+'\n'+'code: '+str(mdata['data'][0]['code'])+'\n'+'ptt: '+str(mdata['data'][0]['rating']/100)

        await arc.finish(snd_msg)





