# -*- coding: utf-8 -*-

from LineAPI.linepy import *
from LineAPI.akad.ttypes import Message
from LineAPI.akad.ttypes import ContentType as Type
from gtts import gTTS
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from googletrans import Translator
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, urllib, urllib3, urllib.parse, traceback, atexit
import traceback
import subprocess


msg_dict = {}

with open('ctoken.json', 'r') as fp:
    akun = json.load(fp)
try:
    client = LINE(akun['master'])
except:
    client = LINE()

print(("F-Bot: ") + client.profile.mid)
akun['master'] = client.authToken
with open('ctoken.json', 'w') as fp:
    json.dump(akun, fp, sort_keys=True, indent=4)

print("😛ล็อคเชลละคับ😛")

mid = client.getProfile().mid
clientmid = client.profile.mid
clientProfile = client.getProfile()
clientSettings = client.getSettings()
clientPoll = OEPoll(client)

contact = client.getProfile()
backup = client.getProfile()
backup.displayName = contact.displayName
backup.pictureStatus = contact.pictureStatus


#=========================================================#
settings = {
    'alwayread':False,
    'autoBlock':False,
    'welcomepic':False,
    'welcomemessage':False,
    'autoadd':False,
    'messageadd':"",
    'autotag':False,
    'tagmessage':"",
    "kickMention": True,
    "kickMention": False,
    "autoAdd": False,
    "autoJoin": False,
    "autoLeave": False,
    "autoRead": False,
    "autoRespon": False,
    "autoJoinTicket": False,
    "checkContact": False,
    "checkPost": False,
    "checkSticker": False,
    "changePictureProfile": False,
    "changeGroupPicture": [],
    "keyCommand": "",
    "myProfile": {
        "displayName": "",
        "coverId": "",
        "pictureStatus": "",
        "statusMessage": ""
    },
    "mimic": {
        "copy": False,
        "status": False,
        "target": {}
    },
    "setKey": False,
    "unsendMessage": False
}

read = {
    "ROM": {},
    "readPoint": {},
    "readMember": {},
    "readTime": {}
}

try:
    with open("Log_data.json","r",encoding="utf_8_sig") as f:
        msg_dict = json.loads(f.read())
except:
    print("Couldn't read Log data")
settings["myProfile"]["displayName"] = clientProfile.displayName
settings["myProfile"]["statusMessage"] = clientProfile.statusMessage
settings["myProfile"]["pictureStatus"] = clientProfile.pictureStatus
coverId = client.getProfileDetail()["result"]["objectId"]
settings["myProfile"]["coverId"] = coverId

#===========================================#

def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@zeroxyuuki "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

def delete_log():
    ndt = datetime.now()
    for data in msg_dict:
        if (datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > timedelta(1):
            if "path" in msg_dict[data]:
                client.deleteFile(msg_dict[data]["path"])
            del msg_dict[data]

def restartBot():
    print ("[ INFO ] BOT RESTART")
    python = sys.executable
    os.execl(python, python, *sys.argv)
def command(text):
    pesan = text.lower()
    if settings["setKey"] == True:
        if pesan.startswith(settings["keyCommand"]):
            cmd = pesan.replace(settings["keyCommand"],"")
        else:
            cmd = "Undefined command"
    else:
        cmd = text.lower()
    return cmd
    
def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("logError.txt","a") as error:
        error.write("\n[ {} ] {}".format(str(time), text))

def helpmessage():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpMessage =   "😤คำสั่ง🙃" + "\n" + \
                    "👽" + key + "-คท" + "\n" + \
                    "👻" + key + "-มิด" + "\n" + \
                    "😷" + key + "-Sp" + "\n" + \
                    "😧" + key + "-Retoken" + "\n" + \
                    "😦" + key + "-เช็คกลุ่ม" + "\n" + \
                    "😞" + key + "mic (พิมคำออกเป็นภาพ)" + "\n" + \
                    "🙃" + key + "kk ⇨ค้นหา" + "\n" + \
                    "😖" + key + "name เปลี่ยนชื่อ" + "\n" + \
                    "🤒" + key + "sh *" + "\n" + \
                    "😨" + key + "myname" + "\n" + \
                    "🤑" + key + "mypict" + "\n" + \
                    "😔" + key + "mybio" + "\n" + \
                    "😓" + key + "mycover" + "\n" + \
                    "👾self bot MIC 👾"
    return helpMessage

def clientBot(op):
    try:
        if op.type == 0:
            #print ("[ 0 ] END OF OPERATION")
            return

        if op.type == 25:
            try:
                print ("[ 25 ] SEND MESSAGE")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                mini = msg.text.lower()
                setKey = settings["keyCommand"].title()
                if settings["setKey"] == False:
                    setKey = ''
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != client.profile.mid:

                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if msg.contentType == 0:
                        if text is None:
                            return
                        else:
                            cmd = command(text)
                            if cmd == "/help":
                                helpMessage = helpmessage()
                                client.sendMessage(to, str(helpMessage))
#============================×==============================================#
                            elif "/sh " in msg.text.lower():
                                spl = re.split("/sh ",msg.text,flags=re.IGNORECASE)
                                if spl[0] == "":
                                    try:
                                        client.sendMessage(msg.to,subprocess.getoutput(spl[1]))
                                    except:
                                        pass
                            elif cmd == "/gi":
                                group = clinet.getGroup(msg.to)
                                path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                                clinet.sendImageWithURL(msg.to,path)



                            elif text.lower() == '/gpict':
                                group = client.getGroup(to)
                                path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                                client.sendImageWithURL(to, path)

#===========================================================================#
                            elif "/name " in msg.text.lower():
                              spl = re.split("/name ",msg.text,flags=re.IGNORECASE)
                              if spl[0] == "":
                                 prof = client.getProfile()
                                 prof.displayName = spl[1]
                                 client.updateProfile(prof)
                                 client.sendMessage(msg.to,"⇨เปลี่ยนชื่อสำเร็จแล้ว⇦")




                            elif cmd == '/mid':
                              client.sendMessage(to,"「ID」\n" +  clientmid)

                            elif cmd.startswith("/im "):
                                    sep = msg.text.split(" ")
                                    textnya = msg.text.replace(sep[0] + " ","")
                                    path = "http://chart.apis.google.com/chart?chs=480x80&cht=p3&chtt=" + textnya + "&chts=FFFFFF,70&chf=bg,s,000000"
                                    client.sendImageWithURL(msg.to,path)

                            if text.lower() == '/cg ':
                                client.sendMessage(to, "กำลังตรวจสอบข้อมูล...")
                                G = client.getGroupIdsJoined()
                                cgroup = client.getGroups(G)
                                ngroup = ""
                                for x in range(len(cgroup)):
                                    gMembMids = [contact.mid for contact in cgroup[x].members]
                                    if receiver in gMembMids:
                                        ngroup += "\n۞➢ " + cgroup[x].name + " | สมาชิก: " + str(len(cgroup[x].members))    
                                if ngroup == "":
                                    client.sendMessage(to, "ไม่พบคุณอยู่ในกลุ่ม")
                                else:
                                    client.sendMessage(to, "۞➢ตรวจพบอยู่ในกลุ่ม %s\n"%(ngroup))
                            if mini == 'retoken':
                                client.sendMessage(to, "ใช้มือจิ้ม กดออกอุปกรณ์ เอาสิ \n line://nv/connectedDevices/")
                            elif "/cg " in text.lower():
                                client.sendMessage(to, "กำลังตรวจสอบข้อมูล...")
                                if 'MENTION' in msg.contentMetadata.keys() != None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    G = client.getGroupIdsJoined()
                                    cgroup = client.getGroups(G)
                                    ngroup = ""
                                    for mention in mentionees:
                                      for x in range(len(cgroup)):
                                        gMembMids = [contact.mid for contact in cgroup[x].members]
                                        if mention['M'] in gMembMids:
                                            ngroup += "\n۞➢ " + cgroup[x].name + " | สมาชิก: " + str(len(cgroup[x].members))    
                                    if ngroup == "":
                                          client.sendMessage(to, "ไม่พบ")
                                    else:
                                        client.sendMessage(to, "۞➢ตรวจพบอยู่ในกลุ่ม %s\n"%(ngroup))
                            elif cmd == "/sp":
                                     start = time.time()
                                     client.sendMessage(to, "speed test...")
                                     elapsed_time = time.time() - start
                                     client.sendMessage(to, "[ %s Seconds ] [ " % (elapsed_time) + str(int(round((time.time() - start) * 1000)))+" ms ]")

                            elif cmd == "me" or cmd == "/me":
                                client.sendContact(to, sender)
                                client.sendMentionFooter(to, 'hello', sender, "https://line.me/ti/p/~nakap1988", "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName);client.sendMessage(to, client.getContact(sender).displayName, contentMetadata = {'previewUrl': 'http://dl.profile.line-cdn.net/'+client.getContact(sender).pictureStatus, 'i-installUrl': 'https://line.me/ti/p/~nakap1988', 'type': 'mt', 'subText': "SASTOS", 'a-installUrl': 'https://line.me/ti/p/~nakap1988', 'a-installUrl': ' https://line.me/ti/p/~nakap1988', 'a-packageName': 'com.spotify.music', 'countryCode': 'ID', 'a-linkUri': 'https://line.me/ti/p/~nakap1988', 'i-linkUri': 'https://line.me/ti/p/~nakap1988', 'id': 'mt000000000a6b79f9', 'text': 'TOS', 'linkUri': 'https://line.me/ti/p/~nakap1988'}, contentType=19)
                            elif cmd == "/myname":
                                contact = client.getContact(sender)
                                client.sendMessage(to, "[ Display Name ]\n{}".format(contact.displayName))
                            elif cmd == "/mybio":
                                contact = client.getContact(sender)
                                client.sendMessage(to, "[ Status Message ]\n{}".format(contact.statusMessage))
                            elif cmd == "/mypict":
                                contact = client.getContact(sender)
                                client.sendImageWithURL(to,"http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
                            elif cmd == "/myvideo":
                                contact = client.getContact(sender)
                                client.sendVideoWithURL(to,"http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
                            elif cmd == "/mycover":
                                channel = client.getProfileCoverURL(sender)          
                                path = str(channel)
                                client.sendImageWithURL(to, path)
                           elif text.lower() == 'เช็คออน์':
                               timeNow = time.time()
                               runtime = timeNow - botStart
                               runtime = format_timespan(runtime)
                               line.sendMessage(to, "เวลาการทำงานของบอท {}".format(str(runtime)))
                            elif text.lower() == 'ไอดีกลุ่ม':
                                gid = line.getGroup(to)
                                 line.sendMessage(to, "→  ⚔️ " + gid.id + " ←")
                            elif text.lower() == 'รูปกลุ่ม':
                                group = line.getGroup(to)
                                path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                                line.sendImageWithURL(to, path)
                           elif text.lower() == 'ชื่อกลุ่ม':
                               gid = line.getGroup(to)
                               line.sendMessage(to, "→ " + gid.name + " ←")



                            elif "/gg " in msg.text.lower():
                                spl = re.split("/gg ",msg.text,flags=re.IGNORECASE)
                                if spl[0] == "":
                                    if spl[1] != "":
                                        try:
                                            if msg.toType != 0:
                                                client.sendMessage(msg.to,"กำลังรับข้อมูล กรุณารอสักครู่..")
                                            else:
                                                client.sendMessage(msg.from_,"กำลังรับข้อมูล กรุณารอสักครู่..")
                                            resp = BeautifulSoup(requests.get("https://www.google.co.th/search",params={"q":spl[1],"gl":"th"}).content,"html.parser")
                                            text = "ผลการค้นหาจาก Google:\n\n"
                                            for el in resp.findAll("h3",attrs={"class":"r"}):
                                                try:
                                                    tmp = el.a["class"]
                                                    continue
                                                except:
                                                    pass
                                                try:
                                                    if el.a["href"].startswith("/search?q="):
                                                        continue
                                                except:
                                                    continue
                                                text += el.a.text+"\n"
                                                text += str(el.a["href"][7:]).split("&sa=U")[0]+"\n\n"
                                            text = text[:-2]
                                            if msg.toType != 0: 
                                                client.sendMessage(msg.to,str(text))
                                            else:
                                                 client.sendMessage(msg.from_,str(text))
                                        except Exception as e:
                                            print(e)

            except:
                pass

#==============================end====================================================#
        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                else:
                   pass
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
				
        else:
            pass
    except Exception as error:
        logError(error)
        traceback.print_tb(error.__traceback__)

while True:
    try:
        delete_log()
        ops = clientPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                clientBot(op)
                clientPoll.setRevision(op.revision)
    except Exception as error:
        logError(error)
        
def atend():
    print("Saving")
    with open("Log_data.json","w",encoding='utf8') as f:
        json.dump(msg_dict, f, ensure_ascii=False,indent=4,separators=(',', ': '))
    print("BYE")
atexit.register(atend)

def logError(text):
    clinet.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        traceback.print_exc()
