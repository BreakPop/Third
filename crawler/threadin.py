# -*- coding:utf-8 -*-
import requests
import re
import xlsxwriter
from bs4 import BeautifulSoup
from datetime import datetime
import codecs
import threading
import random

# 下载图片
def download_img(imageurl, image_dir, imageName='.jpg'):
    rsp = requests.get(imageurl, stream=True)
    image = rsp.content
    path = image_dir + imageName
    with open(path, 'wb') as file:
        file.write(image)


def crawler(s, i, url, header, image_dir, worksheet, txtfile):
    postData = {"start": i}  # post数据
    res = s.post(url, data=postData, headers=header)  # post
    soup = BeautifulSoup(res.content.decode(), "html.parser")  # BeautifulSoup解析
    table = soup.findAll('table', {"width": "100%"})  # 找到所有图书信息的table
    sz = len(table)  # sz = 25,每页列出25篇文章
    for j in range(1, sz + 1):  # j = 1~25
        sp = BeautifulSoup(str(table[j - 1]), "html.parser")  # 解析每本图书的信息

        imageurl = sp.img['src']  # 找图片链接
        bookurl = sp.a['href']  # 找图书链接
        bookName = sp.div.a['title']
        nickname = sp.div.span  # 找别名
        if (nickname):  # 如果有别名则存储别名否则存’无‘
            nickname = nickname.string.strip()
        else:
            nickname = ""

        notion = str(sp.find('p', {"class": "pl"}).string)  # 抓取出版信息,注意里面的.string还不是真的str类型
        rating = str(sp.find('span', {"class": "rating_nums"}).string)  # 抓取平分数据
        nums = sp.find('span', {"class": "pl"}).string  # 抓取评分人数
        nums = nums.replace('(', '').replace(')', '').replace('\n', '').strip()
        nums = re.findall('(\d+)人评价', nums)[0]
        download_img(imageurl, bookName)  # 下载图片
        book = requests.get(bookurl)  # 打开该图书的网页
        sp3 = BeautifulSoup(book.content, "html.parser")  # 解析
        taglist = sp3.find_all('a', {"class": "  tag"})  # 找标签信息
        tag = ""
        lis = []
        for tagurl in taglist:
            sp4 = BeautifulSoup(str(tagurl), "html.parser")  # 解析每个标签
            lis.append(str(sp4.a.string))

        tag = ','.join(lis)  # 加逗号
        the_img = "D:\\tool\Threading\crawler\\" + bookName + ".jpg"
        writelist = [i + j, bookName, nickname, rating, nums, the_img, bookurl, notion, tag]
        for k in range(0, 9):
            if k == 5:
                worksheet.insert_image(i + j, k, the_img)
            else:
                worksheet.write(i + j, k, writelist[k])
            txtfile.write(str(writelist[k]))
            txtfile.write('\t')
        txtfile.write(u'\r\n')


def main():
    now = datetime.now()  # 开始计时
    print(now)

    txtfile = codecs.open("top2501.txt", 'w', 'utf-8')
    url = "http://book.douban.com/top250?"

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    ]
    ua = random.choice(user_agent_list)
    header = {
        'User-Agent':ua,
        "Referer": "http://book.douban.com/"
    }

    image_dir = "D:\\douban\\image\\"
    # 建立Excel
    workbookx = xlsxwriter.Workbook('D:\douban\\booktop250.xlsx')
    worksheet = workbookx.add_worksheet()
    format = workbookx.add_format()
    # format.set_align('justify')
    format.set_align('center')
    # format.set_align('vjustify')
    format.set_align('vcenter')
    format.set_text_wrap()

    worksheet.set_row(0, 12, format)
    for i in range(1, 251):
        worksheet.set_row(i, 70)
    worksheet.set_column('A:A', 3, format)
    worksheet.set_column('B:C', 17, format)
    worksheet.set_column('D:D', 4, format)
    worksheet.set_column('E:E', 7, format)
    worksheet.set_column('F:F', 10, format)
    worksheet.set_column('G:G', 19, format)
    worksheet.set_column('H:I', 40, format)

    item = ['书名', '别称', '评分', '评价人数', '封面', '图书链接', '出版信息', '标签']
    for i in range(1, 9):
        worksheet.write(0, i, item[i - 1])

    s = requests.Session()  # 建立会话
    s.get(url, headers=header)

    thread = []

    for i in range(0, 250, 25):
        geturl = url + "/start=" + str(i)  # 要获取的页面地址
        print("Now to get " + geturl)
        t = threading.Thread(target=crawler,
                             args=(s, i, url, header, image_dir, worksheet, txtfile))
        thread.append(t)

    for i in range(0, 10):
        thread[i].start()

    for i in range(0, 10):
        thread[i].join()

    end = datetime.now()  # 结束计时
    print(end)
    print("程序耗时： " + str(end - now))
    txtfile.close()
    workbookx.close()


if __name__ == '__main__':
    main()

