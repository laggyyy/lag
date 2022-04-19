import json
import requests
from time import time as timestamp
import urllib.parse
import hmac
from datetime import datetime
from time import sleep
import base64
from json_minify import json_minify
from hashlib import sha1
from amino import objects
from concurrent.futures import  ThreadPoolExecutor
from binascii import hexlify
from os import path
from uuid import UUID
from uuid import uuid4
import random
from os import urandom
import threading
from functools import reduce
from base64 import b85decode, b64decode
from hashlib import sha1
import names
import random
import hmac
import platform,socket,re,uuid 
from ppy import keep_alive
keep_alive()
def sig(data):
        key='f8e7a61ac3f725941e3ac7cae2d688be97f30b93'
        mac = hmac.new(bytes.fromhex(key), data.encode("utf-8"), sha1)
        digest = bytes.fromhex("42") + mac.digest()
        return base64.b64encode(digest).decode("utf-8")
    
def deev():
    hw=(names.get_full_name()+str(random.randint(0,10000000))+platform.version()+platform.machine()+names.get_first_name()+socket.gethostbyname(socket.gethostname())+':'.join(re.findall('..', '%012x' % uuid.getnode()))+platform.processor())
    identifier=sha1(hw.encode('utf-8')).digest()
    key='02b258c63559d8804321c5d5065af320358d366f'
    mac = hmac.new(bytes.fromhex(key), b"\x42" + identifier, sha1)
    return (f"42{identifier.hex()}{mac.hexdigest()}").upper()
#from typing import Union
dictlist=[]
THIS_FOLDER = path.dirname(path.abspath(__file__))
account_file = path.join(THIS_FOLDER, "acc.json")
com = "114426240"
chatId="c56d27f2-8418-4f06-9b3b-7f23597d54a5"
#dictlist.reverse()
 
with open(account_file) as file:
    dictlist= json.load(file)
#com="177958565"
api="https://service.narvii.com/api/v1"
 

def get_total(sid,device):
    headers={
    'Accept-Language': 'en-US', 
    'Content-Type': 'application/json; charset=utf-8', 
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1; LG-UK495 Build/MRA58K; com.narvii.amino.master/3.3.33180)', 
    'Host': 'service.narvii.com', 
    'Accept-Encoding': 'gzip',
    'Connection': 'Keep-Alive',
    }
    headers["NDCAUTH"] = f"sid={sid}"
    headers["NDCDEVICEID"]=device
    response = requests.get(f"{api}/g/s/wallet", headers=headers)
    resp=json.loads(response.text)
    #print(resp)
    coins=resp["wallet"]["totalCoins"]
    
    return coins
 
def decode_sid(sid: str) -> dict:
    return json.loads(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), sid + "=" * (-len(sid) % 4)).encode())[1:-20].decode())
 
def sid_to_uid(SID: str) -> str: return decode_sid(SID)["2"]
 
 
 

 
def collect(sid,coins,em,device,com,chatId):
    headers = {
            #"NDCDEVICEID": '223B063D54BEB7463B92A073735DB6F26EFD413010CCF78271F5953F8BB9010FCFF94D3FF917CB98DE',
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.1; LG-UK495 Build/MRA58K; com.narvii.amino.master/3.4.33587)',
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }
    
    headers["NDCAUTH"] = f"sid={sid}"
    headers["NDCDEVICEID"]=device
 
    transactionId = str(UUID(hexlify(urandom(16)).decode('ascii')))
    data = {
            "coins": coins,
            "tippingContext": {"transactionId": transactionId},
            "timestamp": int(timestamp() * 1000)
        }
    data = json.dumps(data)
    headers["NDC-MSG-SIG"]=sig(data)
    headers["Content-Length"] = str(len(data))
    url = f"{api}/x{com}/s/chat/thread/{chatId}/tipping"
    
    response = requests.post(url, headers=headers, data=data)
    resp=json.loads(response.text)
    #print(resp)
    if resp['api:message']=='OK':
            print(f'collected {coins}')
    else:
        print(resp['api:message'])
        print(f'--X {coins} X--  {em}')
 
def login_custom(email: str, secret: str,device:str,devvv:str):
        headers = {
            #"NDCDEVICEID": '223B063D54BEB7463B92A073735DB6F26EFD413010CCF78271F5953F8BB9010FCFF94D3FF917CB98DE',
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.1; LG-UK495 Build/MRA58K; com.narvii.amino.master/3.4.33587)',
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }
        data = json.dumps({
            "email": email,
            # "phoneNumber":email,
            "v": 2,
            "secret":f"{secret}",
            "deviceID":device,
            "clientType": 100,
            "action": "normal",
            "timestamp": int(timestamp() * 1000)
        })
        headers["NDC-MSG-SIG"]=sig(data)
        headers["NDCDEVICEID"]=devvv
        proxies={
        "http": "http://15ee19bc5e9a4fab9df4b28519077eda:@proxy.crawlera.com:8011/",
        "https": "http://15ee19bc5e9a4fab9df4b28519077eda:@proxy.crawlera.com:8011/",
    }
        response = requests.post(f"{api}/g/s/auth/login", headers=headers, data=data,proxies=proxies,verify=False)
        
        resp=json.loads(response.text)
        #rint(resp)
        if resp["api:statuscode"]==0:
 
          #sec=resp["secret"]
          sid=resp['sid']
        else:
          print(resp["api:statusco"])
        return sid
 

 
def set_once(sid,dev,com):
        headers = {
            #"NDCDEVICEID": '223B063D54BEB7463B92A073735DB6F26EFD413010CCF78271F5953F8BB9010FCFF94D3FF917CB98DE',
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.1; LG-UK495 Build/MRA58K; com.narvii.amino.master/3.4.33587)',
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }
        #p=get_com(dev)
        headers["NDCAUTH"]=f'sid={sid}'
        headers["NDCDEVICEID"]=dev
        
         
        data = {"timestamp": int(timestamp() * 1000)}
        #print(get)
        data = json.dumps(data)
        headers["NDC-MSG-SIG"]=sig(data)
        response=requests.post(f"{api}/x{com}/s/community/join?sid={sid}", data=data, headers=headers)
        #print("fff")
        #print(response.text)

def leave_community(comId,sid,dev):
  headers = {
            #"NDCDEVICEID": '223B063D54BEB7463B92A073735DB6F26EFD413010CCF78271F5953F8BB9010FCFF94D3FF917CB98DE',
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.1; LG-UK495 Build/MRA58K; com.narvii.amino.master/3.4.33587)',
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }
        #p=get_com(dev)
  headers["NDCAUTH"]=f'sid={sid}'
  headers["NDCDEVICEID"]=dev
  data ={"timestamp": int(timestamp() * 1000)}
  data = json.dumps(data)
  headers["NDC-MSG-SIG"]=sig(data)
  p=requests.post(f"{api}/x{comId}/s/community/leave?sid={sid}", data = data, headers =headers)
  #print(p.text)
 

def gen_1(account):
        #r=random.randint(1,5)
        sleep(2)
        
        devv=account["device"]
        dev=deev()
        sid=login_custom(account['email'],account['secret'],devv,dev)
 
        #print(sid)
        m=account['email']
        set_once(sid, dev,com)
        coins=get_total(sid,dev)
        print(f'Available {m} {coins}')
        while coins>500:
          try:
            collect(sid,500,m,deev(),com,chatId)
          except Exception as d:
            print(d)
          coins=coins-500
        if coins!=0:
          try:
            collect(sid,coins,m,deev(),com,chatId)
          except Exception as k:
            print(k)
        
        #leave_community(com,sid,dev)
        
        # with ThreadPoolExecutor(max_workers=25) as executor:
            # _ = [executor.submit(gen,sid,i,m) for i in range(1,26,1)]
 
def main():
    with ThreadPoolExecutor(max_workers=100) as executor:
        _ = [executor.submit(gen_1, em) for em in dictlist]
    print("Completed")
 
if __name__ == '__main__': # Running main function in standalone
    main()
