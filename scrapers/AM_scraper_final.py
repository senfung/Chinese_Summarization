### use this code for scraping
### AM daily news

import re
from time import sleep
import json
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

local_news_url = 'https://www.am730.com.hk/news/share/'


for i in range(158097,100000,-1):

    url = local_news_url + str(i);

    print(url)

    try:
        page = urllib.request.urlopen(url)

        soup = BeautifulSoup(page, 'html.parser')

        title_box = soup.find('div',attrs={'class':'news-detail-title'})
        title = title_box.text.strip()


        content_box = soup.find('div',attrs={'class':'news-detail-content'})
        content_soup = BeautifulSoup(str(content_box), 'html.parser')
        content_box = content_soup.find_all('p')

        content=''
        for c_b in content_box:
            c = c_b.text.strip()
            content = content + c +'\n'

        category_box = soup.find('section',attrs={'id':'news-detail-page-title'})
        category_soup = BeautifulSoup(str(category_box), 'html.parser')
        category_box = category_soup.find('a',attrs={'class':'aBlack'})
        category = category_box.text.strip()

    except:
        print("no article with this url")
        continue

    print(category)

    a = {"id": i, "url": url, "title": title, "content": content}

    if(category == "News"):
        f = open("AM_local_china_inter.txt", "a+", encoding='utf-8')
    elif(category == "Finance"):
        f = open("AM_fin_estate.txt", "a+", encoding='utf-8')
    elif(category == "Sport"):
        f = open("AM_sports.txt", "a+", encoding='utf-8')
    else:
        continue

    f.write(json.dumps(a,ensure_ascii=False))
    f.write('\n')
    f.close()

    print("Article " + title + " saved to file")
    print()

    sleep(1)



    
