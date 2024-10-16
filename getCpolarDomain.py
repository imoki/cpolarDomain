"""
    作者：imoki
    仓库：https://github.com/imoki
    功能：动态获取cpolar的当前域名并写入publicurl.txt文件中
    版本：v1.0.0
    时间：上古时期
"""

import requests
import json

# 不要泄露了，这个账号和密码。填写你的账号和密码
data = {"email":"xxx@xxx.com","password":"xxxx"}

url = "http://localhost:9200"
suffixLogin = "/api/v1/user/login"

headerLogin = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': url,
    'Referer': url,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0'
}

proxies = {
    'http': 'http://localhost:8080',
    'https': 'http://localhost:8080'
}


suffixTunnels = "/api/v1/tunnels"


def getToken():
    reponse = requests.post(url = url+suffixLogin, headers = headerLogin, json = data)#, proxies=proxies)
    reponse = json.loads(reponse.text)
    reponse = reponse['data']['token']
    #print(reponse)
    return reponse.strip()

def getPublicUrl():
    token = getToken()
    headerToken = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55',
        'Authorization': ': Bearer ' + token,
        'Referer': url,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0'
    }
    reponse = requests.get(url = url+suffixTunnels, headers = headerToken)
    reponse = json.loads(reponse.text)
    #print(reponse)
    reponse = reponse['data']['items'][0]['public_url']
    return reponse.strip()
    
    
if __name__ == "__main__":
    publicUrl = getPublicUrl()
    with open("publicurl.txt", "w" ,encoding='utf-8') as f:
        f.write(publicUrl)
    
    
