### use this code for scraping
### SP daily news

import re
from time import sleep
import json
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

local_news_url = 'https://skypost.ulifestyle.com.hk/article/'


for i in range(2252600,2100000,-1):

    url = local_news_url + str(i) + '/';

    print(url)

    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        title_box = soup.find('h1')
        content_box = soup.find('div',attrs={'class':'article-details-content-container'})
        category_box = soup.find('ul', attrs={'class':'sectionName'})

        title = title_box.text.strip()
        content = content_box.text.strip()
        category = category_box.text.strip()

    except:
        print("no article with this url")
        continue

    print(category)

    a = {"id": i, "url": url, "title": title, "content": content}

    if(category == "港聞"):
        f = open("SP_local.txt", "a+", encoding='utf-8')
    elif(category == "財經/地產"):
        f = open("SP_fin_estate.txt", "a+", encoding='utf-8')
    elif(category == "中國/國際"):
        f = open("SP_china_inter.txt", "a+", encoding='utf-8')
    elif(category == "體育"):
        f = open("SP_sports.txt", "a+", encoding='utf-8')
    else:
        continue

    f.write(json.dumps(a,ensure_ascii=False))
    f.write('\n')
    f.close()

    print("Article " + title + " saved to file")
    print()

    sleep(1)
