### use this code for scraping
### XT daily news

import re
from time import sleep
import json
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

local_news_url = 'http://std.stheadline.com/daily/article/detail/'
# Range:985695-1938994
# Testing Range: 985695 - 985695 + 3*3
# 1937455
for i in range(1938994,985695,-3):

    url = local_news_url + str(i) + '-';
    #url = "http://std.stheadline.com/instant/articles/detail/900205-%E9%A6%99%E6%B8%AF-%E3%80%90%E5%9C%9F%E5%9C%B0%E5%A4%A7%E8%BE%AF%E8%AB%96%E3%80%91%E7%92%B0%E4%BF%9D%E8%A7%B8%E8%A6%BA%E6%89%B9%E7%82%BA%E9%85%8D%E5%90%88%E6%98%8E%E6%97%A5%E5%A4%A7%E5%B6%BC+%E5%B0%88%E8%B2%AC%E5%B0%8F%E7%B5%84%E6%9B%B2%E8%A7%A3%E6%B0%91%E6%84%8F"
    print(url)

    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        title_box = soup.find('h1')
        content_box = soup.find('div',attrs={'class':'post-content'})
        category_box = soup.find('h3')

        title = title_box.text.strip()

        content_box = re.sub(r'<div class="carousel-caption">(.+)</div>', "", str(content_box))
        soup = BeautifulSoup(content_box, 'html.parser')
        content_box = soup.find('div',attrs={'class':'post-content'})
        content = content_box.text.strip()

        category = category_box.text.strip()
    except:
        print("no article with this url")
        continue

    print(category)

    a = {"id": i, "url": url, "title": title, "content": content}

    if(category == "要聞港聞"):
        f = open("XT_local.txt", "a+", encoding='utf-8')
    elif(category == "財經新聞"):
        f = open("XT_fin.txt", "a+", encoding='utf-8')
    elif(category == "中國新聞"):
        f = open("XT_china.txt", "a+", encoding='utf-8')
    elif(category == "國際新聞"):
        f = open("XT_inter.txt", "a+", encoding='utf-8')
    elif(category == "教育新聞"):
        f = open("XT_edu.txt", "a+", encoding='utf-8')
    elif(category == "地產新聞"):
        f = open("XT_estate.txt", "a+", encoding='utf-8')
    elif(category == "體育新聞"):
        f = open("XT_sports.txt", "a+", encoding='utf-8')
    else:
        continue

    f.write(json.dumps(a,ensure_ascii=False))
    f.write('\n')
    f.close()

    print("Article " + title + " saved to file")
    print()

    sleep(1)
