# coding:UTF8
import sys

reload(sys)

sys.setdefaultencoding('utf8')


import urllib
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup
import string

import chardet
import time



print "begein"
url_model = "http://www.yidukindle.com/"
webname_login = "tem_web_login.html"
webname_researchbook = "tem_web_login&searchbook.html"


def write_in_file(data, fileurl, model = "w"):
    file = open(fileurl, model)
    file.write(data)
    file.close()

def read_from_file(fileurl):
    file = open(fileurl,"r")
    content = file.read()
    file.close()
    return content

def login():
    hosturl = "http://www.yidukindle.com/login.php"
    posturl = "http://www.yidukindle.com/login.php"


    # 建立cookie处理器
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    print "cookie loaded"

    # 打开登陆页面，下载需要的cookie
    h = urllib2.urlopen(hosturl)

    headers = {
        'Host': 'www.yidukindle.com',
        'Connection': 'keep-alive',
        'Content-Length': '69',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://www.yidukindle.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.yidukindle.com/login.php',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    postdata = {
        "useremail":"matthew9602@qq.com",
        "userpwd":"yidu07n0604",
        "remember[]":"yes"
    }

    postdata = urllib.urlencode(postdata)
    request = urllib2.Request(posturl,postdata,headers)
    print request
    response =  urllib2.urlopen(request)
    print "login code:", response.getcode()
    text = response.read()
    write_in_file(text,webname_login,"w")

def openurl(url):
    response = urllib2.urlopen(url)
    write_in_file(response.read(),"tem_web.html","w")
    return response

def check_refresh(str):
    soup = BeautifulSoup(str, "html5lib")
    tables = soup.find_all("table","table table-hover table-bordered")
    content_table = tables[1]
    first_book = content_table.tbody.tr
    bookname = first_book.find_all("td")[1].div.span.string
    write_in_file(bookname,"txt_transfer.txt","w")
    bookname = read_from_file("txt_transfer.txt")
    name_lasttime = read_from_file("lasttime_bookname.txt")
    # print name_lasttime, type(name_lasttime)
    # print bookname, type(bookname)
    # print "name_lasttime", chardet.detect(name_lasttime)
    # print "bookname", chardet.detect(bookname)
    return name_lasttime != bookname

def download_new_magain(str):
    soup = BeautifulSoup(str, "html5lib")
    first_book = soup.find_all("table", "table table-hover table-bordered")[1].tbody.tr
    bookname = first_book.find_all("td")[1].div.span.string
    book_urls = first_book.find_all('a', 'btn btn-primary btn-sm ')
    book_url_pdf = url_model + book_urls[2].attrs["href"]
    print "download from url: ", book_url_pdf
    response = urllib2.urlopen(book_url_pdf)
    realurl = response.geturl()
    print "real book url:", realurl
    urllib.urlretrieve(realurl, bookname+".mobi")
    print "download completed"

if __name__ == '__main__':
    login()

    hosturl = "http://www.yidukindle.com/magzine.list.php?magid=60"
    response = urllib2.urlopen(hosturl)
    print "book get code: ", response.getcode()
    response_book_content = response.read()

    # write_in_file(response_book_content,webname_researchbook)
    if check_refresh(response_book_content):
        download_new_magain(response_book_content)
    else:
        print "book downloaded"
    openurl(url_model+"exit.php")

