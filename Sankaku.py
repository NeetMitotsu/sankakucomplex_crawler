import Http
from bs4 import BeautifulSoup
import Log
import re

def get_html_list(page: int = 1, tags: str = '', next: int = 0):
    """
    获取列表页html源码
    :param page: 页数
    :param tags: 爬取关键词
    :param next: 下个的id
    :return: str
    """
    url = 'https://chan.sankakucomplex.com/post/index.content?'
    tmp_tag = 'tags='
    tmp_next = 'next='
    if next != 0:
        tmp_next += tmp_next + next
    if tags != '':
        tmp_tag += tags
    url += tmp_next + '&' + tmp_tag + '&' + 'page=' + str(page)
    # print(url)
    html = Http.get(url)
    if not html:
        Log.add('抓取<' + url + '>' + '失败')
        exit()
    try:
        html = html.decode('utf8')
    except:
        Log.add('解码失败')
        exit(500)
    return html

def get_inner_atag(html: str):
    """
    获取内部大图的a标签列表
    :param html: html列表页源码
    :type html: str
    :return: list
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('a')

def get_inner_ahref(atag):
    """
    获取a标签的href
    :param a: a标签源码
    :return: str
    """
    return atag['href']

def get_inner_url_id(ahref: str):
    """
    获取每幅图的id
    :param ahref: a标签的href
    :return: str
    """
    return re.findall(r'\d{1,}', ahref)[0]

def get_inner_html(inner_ahref: str):
    """
    根据内部url获取内部html源码
    :param inner_ahref:
    :type inner_ahref: str
    :return:
    """
    url = "https://chan.sankakucomplex.com" + inner_ahref
    html = Http.get(url)
    if not html:
        Log.add('抓取<' + url + '>' + '失败')
        exit()
    try:
        html = html.decode('utf8')
    except:
        Log.add('解码失败')
        exit(500)
    return html

def get_info(inner_html):
    """
    获取详情
    :param inner_html: 详图的html源码
    :type inner_html: str
    :return: list
    """
    soup = BeautifulSoup(inner_html, 'html.parser')
    img = soup.find('a',id = 'image-link').find('img')
    return {'height':img['height'], 'width':img['width'], 'src':img['src']}