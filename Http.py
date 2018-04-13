import urllib.request
import requests

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


retry_count = 5
proxy_addr = get_proxy()
proxy = urllib.request.ProxyHandler({'http':proxy_addr})
opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)


def get(url: str, header: list = {}):
    global retry_count, proxy_addr
    """
    Http Get获取
    :param url: URL地址
    :param header: HTTP头
    :return: row
    """
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    header['Accept-Language'] = 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6'
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    # header['Host'] = 'chan.sankakucomplex.com'
    # print(header)
    request = urllib.request.Request(url, headers = header)
    while retry_count > 0:
        try:
            return urllib.request.urlopen(request).read()
        except Exception:
            retry_count -= 1
    delete_proxy(proxy_addr)
    # proxy_addr = get_proxy()
    # retry_count = 5
    return None



