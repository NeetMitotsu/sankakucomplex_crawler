# coding:utf-8
'''''
   function：爬取百度百科所有北京景点，
   author:yi
'''
import urllib.request
from urllib.request import urlopen
from urllib.error import HTTPError
import urllib.parse
from bs4 import BeautifulSoup
import re
import codecs
import json


class BaikeCraw(object):
    def __init__(self):
        self.urls = set()
        self.view_datas = {}

    def craw(self, filename):
        urls = self.getUrls(filename)
        if urls == None:
            print("not found")
        else:
            for urll in urls:
                print(urll)
                try:
                    html_count = self.download(urll)
                    self.passer(urll, html_count)
                except:
                    print("view do not exist")
                '''''file=self.view_datas["view_name"] 
                self.craw_pic(urll,file,html_count) 
                 print(file)'''

    def getUrls(self, filename):
        new_urls = set()
        file_object = codecs.open(filename, encoding='utf-16', )
        try:
            all_text = file_object.read()
        except:
            print("文件打开异常！")
            file_object.close()
        file_object.close()
        view_names = all_text.split(" ")
        for l in view_names:
            if '﻿' in l:
                view_names.remove(l)
        for l in view_names:
            '''''http://baike.baidu.com/search/word?word='''  # 得到url的方法
            name = urllib.parse.quote(l)
            name.encode('utf-8')
            url = 'http://baike.baidu.com/search/word?word=' + name
            new_urls.add(url)
        print(new_urls)
        return new_urls

    def manger(self):
        pass

    def passer(self, urll, html_count):
        soup = BeautifulSoup(html_count, 'html.parser', from_encoding='utf_8')
        self._get_new_data(urll, soup)
        return

    def download(self, url):
        if url is None:
            return None
        response = urllib.request.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read()

    def _get_new_data(self, url, soup):  ##得到数据
        if soup.find('div', class_="main-content").find('h1') is not None:
            self.view_datas["view_name"] = soup.find('div', class_="main-content").find('h1').get_text()  # 景点名
            print(self.view_datas["view_name"])
        else:
            self.view_datas["view_name"] = soup.find("div", class_="feature_poster").find("h1").get_text()
        self.view_datas["view_message"] = soup.find('div', class_="lemma-summary").get_text()  # 简介
        self.view_datas["basic_message"] = soup.find('div', class_="basic-info cmn-clearfix").get_text()  # 基本信息
        self.view_datas["basic_message"] = self.view_datas["basic_message"].split("\n")
        get = []
        for line in self.view_datas["basic_message"]:
            if line != "":
                get.append(line)
        self.view_datas["basic_message"] = get
        i = 1
        get2 = []
        tmp = "%%"
        for line in self.view_datas["basic_message"]:

            if i % 2 == 1:
                tmp = line
            else:
                a = tmp + ":" + line
                get2.append(a)
            i = i + 1
        self.view_datas["basic_message"] = get2
        self.view_datas["catalog"] = soup.find('div', class_="lemma-catalog").get_text().split("\n")  # 目录整体
        get = []
        for line in self.view_datas["catalog"]:
            if line != "":
                get.append(line)
        self.view_datas["catalog"] = get
        #########################百科内容
        view_name = self.view_datas["view_name"]
        html = urllib.request.urlopen(url)
        soup2 = BeautifulSoup(html.read(), 'html.parser').decode('utf-8')
        p = re.compile(r'<div class="para-title level-2"', re.DOTALL)
        r = p.search(soup2)
        content_data_node = soup2[r.span(0)[0]:]  # 第一个h2（头）
        p = p = re.compile(r'<div class="album-list">', re.DOTALL)  # 尾
        r = p.search(content_data_node)
        content_data = content_data_node[0:r.span(0)[0]]
        lists = content_data.split('<div class="para-title level-2">')
        i = 1
        for list in lists:  # 每一大块
            final_soup = BeautifulSoup(list, "html.parser")
            name_list = None
            try:
                part_name = final_soup.find('h2', class_="title-text").get_text().replace(view_name, '').strip()
                part_data = final_soup.get_text().replace(view_name, '').replace(part_name, '').replace('编辑',
                                                                                                        '')  # 历史沿革
                name_list = final_soup.findAll('h3', class_="title-text")
                all_name_list = {}
                na = "part_name" + str(i)
                all_name_list[na] = part_name
                final_name_list = []  ###########
                for nlist in name_list:
                    nlist = nlist.get_text().replace(view_name, '').strip()
                    final_name_list.append(nlist)
                fin = "final_name_list" + str(i)
                all_name_list[fin] = final_name_list
                print(all_name_list)
                i = i + 1
                # 正文
                try:
                    p = re.compile(r'<div class="para-title level-3">', re.DOTALL)
                    final_soup = final_soup.decode('utf-8')
                    r = p.search(final_soup)
                    final_part_data = final_soup[r.span(0)[0]:]
                    part_lists = final_part_data.split('<div class="para-title level-3">')
                    for part_list in part_lists:
                        final_part_soup = BeautifulSoup(part_list, "html.parser")
                        content_lists = final_part_soup.findAll("div", class_="para")
                        for content_list in content_lists:  # 每个最小段
                            try:
                                pic_word = content_list.find("div",
                                                             class_="lemma-picture text-pic layout-right").get_text()  # 去掉文字中的图片描述
                                try:
                                    pic_word2 = content_list.find("div",
                                                                  class_="description").get_text()  # 去掉文字中的图片描述
                                    content_list = content_list.get_text().replace(pic_word, '').replace(pic_word2, '')
                                except:
                                    content_list = content_list.get_text().replace(pic_word, '')

                            except:
                                try:
                                    pic_word2 = content_list.find("div",
                                                                  class_="description").get_text()  # 去掉文字中的图片描述
                                    content_list = content_list.get_text().replace(pic_word2, '')
                                except:
                                    content_list = content_list.get_text()
                            r_part = re.compile(r'\d.|\d')
                            part_result, number = re.subn(r_part, "", content_list)
                            part_result = "".join(part_result.split())
                            # print(part_result)
                except:
                    final_part_soup = BeautifulSoup(list, "html.parser")
                    content_lists = final_part_soup.findAll("div", class_="para")
                    for content_list in content_lists:
                        try:
                            pic_word = content_list.find("div",
                                                         class_="lemma-picture text-pic layout-right").get_text()  # 去掉文字中的图片描述
                            try:
                                pic_word2 = content_list.find("div", class_="description").get_text()  # 去掉文字中的图片描述
                                content_list = content_list.get_text().replace(pic_word, '').replace(pic_word2, '')
                            except:
                                content_list = content_list.get_text().replace(pic_word, '')

                        except:
                            try:
                                pic_word2 = content_list.find("div", class_="description").get_text()  # 去掉文字中的图片描述
                                content_list = content_list.get_text().replace(pic_word2, '')
                            except:
                                content_list = content_list.get_text()
                        r_part = re.compile(r'\d.|\d')
                        part_result, number = re.subn(r_part, "", content_list)
                        part_result = "".join(part_result.split())
                        # print(part_result)

            except:
                print("error")
        return

    def output(self, filename):
        json_data = json.dumps(self.view_datas, ensure_ascii=False, indent=2)
        fout = codecs.open(filename + '.json', 'a', encoding='utf-16', )
        fout.write(json_data)
        # print(json_data)
        return

    def craw_pic(self, url, filename, html_count):
        soup = BeautifulSoup(html_count, 'html.parser', from_encoding='utf_8')
        node_pic = soup.find('div', class_='banner').find("a", href=re.compile("/photo/poi/....\."))
        if node_pic is None:
            return None
        else:
            part_url_pic = node_pic['href']
            full_url_pic = urllib.parse.urljoin(url, part_url_pic)
            # print(full_url_pic)
        try:
            html_pic = urlopen(full_url_pic)
        except HTTPError as e:
            return None
        soup_pic = BeautifulSoup(html_pic.read())
        pic_node = soup_pic.find('div', class_="album-list")
        print(pic_node)
        return


if __name__ == "__main__":
    spider = BaikeCraw()
    filename = "D:\\Pycharm_WorkSpace\\sankakucomplex\\view_points_part.txt"
    spider.craw(filename)