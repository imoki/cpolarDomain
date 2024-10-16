"""
    作者：imoki
    仓库：https://github.com/imoki
    功能：动态获取cpolar的当前域名并写将域名提交到github仓库的CNAME文件中，从而实现动态修改CNAME文件的效果，可用于github建站。
    版本：v1.0.0
    时间：上古时期
"""

from github import Github
import requests
import json
from urllib.parse import urlsplit



# 不要泄露了，这个账号和密码。填写你的账号和密码
data = {"email":"xxx@xxx.com","password":"xxxx"}

# 不要泄露了，github的access token。填写你的github的access token
g = Github("github_xxx_xxxxxxxx")


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
    print("获取CNAME")
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
    
# 提交git，修改CNAME
def gitcommit(content):
    print("更新CNAME")
    for repo in g.get_user().get_repos():
        #print(repo)
        print(repo.name)
        # 文档https://pygithub.readthedocs.io/en/latest/examples/Repository.html#update-a-file-in-the-repository
        #repo.create_file("CNAME", "commit content", "hi", branch="main") # 创建文件
        
        # 更新文件
        contents = repo.get_contents("CNAME", ref="main")
        repo.update_file(contents.path, "update", content, contents.sha, branch="main")

# 只取出域名
def get_domain(url):
    print("格式化CNAME")
    if "://" not in url:  # or: not re.match("(?:http|ftp|https)://"", url)
        url = f"https://{url}"
    url = urlsplit(url).hostname
    print(url)
    return url

if __name__ == "__main__":
    publicUrl = getPublicUrl()
    #print(publicUrl)
    gitcommit(get_domain(publicUrl))
    #with open("publicurl.txt", "w" ,encoding='utf-8') as f:
    #    f.write(publicUrl)
    
    
    



