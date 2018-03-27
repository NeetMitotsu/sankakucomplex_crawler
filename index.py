import Http
import Function
import Log
import Sankaku
import re
import time

# 页码
page = 1
# 终止页码 此页码为0时根据last_start_id来判断是否停止爬取； 非0时爬完此页即停止
# 参数必须 >= page
max_page = 0

# 保存路径
dic_path = input('输入保存的目录全路径,不存在会创建 (默认地址：E:/SankakuComplex\n')
tags = str(Function.get('last_tags.data'))
# 搜索参数
tmp_tags = input('输入爬取关键字, 多关键字中间用\'_\'连接(例：final_fantasy_14，默认上次搜索的关键词\n 上次搜索关键词为: ' + tags + '\n')

tags = str(Function.get('last_tags.data')) if tmp_tags == '' else tmp_tags

# 创建目录存放今天爬取的图
Function.create_folder(dic_path)
# 上次开始时爬取第一张的图片ID
last_start_id = int(Function.get('last_start_id.data')) if tags == '' else int(Function.get(tags + '.data'))

# 当前第几张
index = 0
# 爬取是否结束
end = False

while True:
    # 终止页码为0 或 未到达终止页码时 才进行爬取
    if max_page == 0 or page <= max_page:
        # 获取页面内容
        Log.add('正在读取第' + str(page) + '页内容')
        list_html = Sankaku.get_html_list(page, tags)
        # 获取第page页的列表
        a_list = Sankaku.get_inner_atag(list_html)
        Function.write('last_tags.data', tags, True)
        # 遍历列表页中的a标签
        for atag in a_list:
            index += 1
            ahref = Sankaku.get_inner_ahref(atag)
            # 获取详情页
            inner_html = Sankaku.get_inner_html(ahref)
            # 获取id
            id = Sankaku.get_inner_url_id(ahref)
            # 获取图片信息
            img_info_list = Sankaku.get_info(inner_html)
            width = img_info_list['width']
            height = img_info_list['height']

            # 存储last_start_id
            if index == 1:
                if len(img_info_list) == 3:
                    Function.write(tags + '.data', id, True)
                else:
                    # 第一个id出现问题, 退出
                    exit()

            # 数据结构是否错误
            if len(img_info_list) != 3:
                Log.add(str(index) + '错误, 跳过')
                continue
            # 已经爬到上次开始爬的地方了 且 终止页码为0 本次爬取结束
            if int(id) == last_start_id and max_page == 0:
                end = True
                break

            download = True  # 是否下载此图
            if download:
                # 获取文件名
                # 此处不解码
                # print(img_info_list['src'])
                imgsrc = re.findall(r"/.*jpg|/.*gif|/.*png|/.*jpeg", img_info_list['src'])[0]
                # print(img_info_list['src'])
                # print(imgsrc)
                file_name = imgsrc.split('/')[-1]
                if Function.exist(file_name):
                    Log.add(imgsrc + '已存在, 跳过')
                    continue

                Log.add(str(index) + '-' + file_name + '开始下载。。。。')
                ts = time.time()
                # print('https:' + imgsrc)
                # print('https://chan.sankakucomplex.com' + ahref)
                img = Http.get('https:' + imgsrc)
                Log.add('下载完毕。耗时：' + str(int(time.time() - ts)) + 's')
                Function.write(file_name, img)
        if end:
            break
    else:
        break
    page += 1

Log.add('爬取结束')
Function.write('log_' + str(int(time.time()))+ '.txt', Log.get())
exit(200)
