# -*- coding: UTF-8 -*-
# Powered by bihu/QQQQQ GitHub/yuzhenqin
# This is a part of bihulib
import requests,time,json,os,sys
requests.packages.urllib3.disable_warnings()
headers = {
    'bihu_api':{
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
        'access-control-request-headers':'authorization,device,nonce,signature,timestamp,uuid,validatetoken,version',
        'access-control-request-method':'GET',
        'origin':'https://bihu.com',
        'referer':'https://bihu.com/',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-site',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        },
    'only_ua':{
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
}
def test_connect():
    return requests.get('https://gw.bihu.com/api/content/hot/list?pageNum=1',headers=headers['bihu_api'],verify=False).status_code
def getHotArticleWithPage(pageNum):
    getPage = requests.get('https://gw.bihu.com/api/content/hot/list?pageNum='+str(pageNum),headers=headers['bihu_api'],verify=False).json()
    return getPage["data"]["data"]
def getAllHotArticle(start,end):
    ret = []
    for i in range(start,int(end)+1):
        getPage = requests.get('https://gw.bihu.com/api/content/hot/list?pageNum='+str(i),headers=headers['bihu_api'],verify=False).json()
        temp = getPage["data"]["data"]
        for j in range(0,len(temp)):
            ret.append(temp[j])
    return ret
def getNewSmallArticleWithPage(pageNum):
    getPage = requests.get('https://gw.bihu.com/api/content/hot/list?pageNum='+str(pageNum)+'&type=SHORT',headers=headers['bihu_api'],verify=False).json()
    return getPage["data"]["data"]
def getAllNewSmallArticle(st,end):
    starttime=time.time()
    ret = []
    for i in range(st,int(end)+1):
        gp = getNewSmallArticleWithPage(i)
        for j in range(0,len(gp)):
            ret.append(gp[j])
        if i%20==0:
            os.system('cls')
    return ret