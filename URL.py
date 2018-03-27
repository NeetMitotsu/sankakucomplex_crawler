import urllib.request
import re

def getHtmlCode(url): # 该方法传入url，返回url的html编码
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
    }
    url1 = urllib.request.Request(url, headers = headers)
    page = urllib.request.urlopen(url1).read()
    page = page.decode('utf8')
    return page

def getImg(page): # 该方法传入html源码，截取img标签，将图片保存到本地
    # findall(正则,代表页面源码的str)函数，在字符串中按照正则表达式截取其中的小字符串
    # findall()返回一个列表,列表中的元素是一个个的元组，元组的第一个元素是图片的url，第二个元素是url的后缀名
    # 列表形如：[('http://www.zhangzishi.cc/732x120.gif', 'gif'), ('http://ww2.sinaimg.cn/qomyo.jpg', 'jpg')
    imgList = re.findall(r'(http:[^\s]*?(jpg|png|gif))"',page)
    x = 0
    for imgUrl in imgList: #列表循环
        print('正在下载: %s'%imgUrl[0])
        # urlretrieve(url,local)方法根据图片的url将图片保存到本机
        urllib.request.urlretrieve(imgUrl[0], 'E:/pythonSpiderFile/img/%d.jpg'%x)
        x+=1

if __name__ == '__main__':
    url = '//cs.sankakucomplex.com/data/10/db/10db08de794f272606191c984bbd6dfa.jpeg?e=1522229157&m=fTtCi1ZIrhmsJHlrdXuzXA'
    str = re.findall(r"/.*jpg|/.*gif|/.*png|/.*jpeg",url)
    print(str)