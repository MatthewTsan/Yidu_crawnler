str = """Host: www.yidukindle.com
Connection: keep-alive
Content-Length: 69
Cache-Control: max-age=0
Origin: http://www.yidukindle.com
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: http://www.yidukindle.com/login.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
"""

headers = {}
str = str.splitlines()
for item in str:
    key, data = item.split(": ")
    headers[key] = data
    print "'" + key + "': '" + data + "',"
# print headers