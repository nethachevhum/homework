import requests
headers = {
    "Host": "www.dorev.ru",
    "Cookie":"XMMGETHOSTBYADDR213134210163=U1%3A+163.210.unused-addr.ncport.ru; XMMcms4siteUSER=1; XMMFREE=YES; XMMPOLLCOOKIE=XMMPOLLCOOKIE",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
}
res = requests.get('http://www.dorev.ru/', headers=headers)
print(res.text)