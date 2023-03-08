from bs4 import BeautifulSoup
import requests
import time
import re
import lxml.html
from lxml.etree import tostring


def chonint(num):
    n = num.replace(",", "")
    # print(n)
    return float(n)


# 株探注目ニュース一覧ページ
url = "https://kabutan.jp/news/marketnews/?category=9"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

# 全てのaタグを検索
for element in soup.find_all("a"):
    # テキストに「今朝」が含まれているか調べる
    if "今朝" in element.text:
        link = element.get("href")
        # print(element.text)
        # urlを出力(urlが不完全なので補完)
        # print("https://kabutan.jp" + link)

# 株探今朝の注目ニュースページ
url = "https://kabutan.jp" + link
# html = requests.get(url)
# soup = BeautifulSoup(html.content, "html.parser")
# print(url)
# news = soup.find_all(class_="body")
# print(news)

# XPath
req = requests.get(url)
html = req.text
dom = lxml.html.fromstring(html)
# div class='body'のxpath
target_xpath = '//*[@id="shijyounews"]/article/div'
scraped_data = dom.xpath(target_xpath)
# list
namelists, codelists, descriptions = [], [], []
for news in scraped_data:
    # news=lxml.html.HtmlElement
    fundamentals = tostring(news, encoding="utf-8").decode().split("&lt;")
    articles = tostring(news, encoding="utf-8").decode().replace("\n", "")
    articles = articles.replace("　【悪材料】　　――――――――――――<br/>", "")
    print(articles)
    # 7行目から3step毎のdescriptionを取得する
    for codelist in articles.split("<br/>")[7::3]:
        # 空要素は除外する
        if codelist != "":
            # 銘柄名一覧
            # print(codelist.split()[0])
            namelists.append(codelist.split()[0])
            # コードURL一覧
            # print(codelist.split('"')[1])
            codelists.append(codelist.split('"')[1])
    # テスト出力
    for i, a in enumerate(namelists):
        print(i, a)
    for i, a in enumerate(codelists):
        print(i, a)

    # print(fundamentals[4].split('"')[1])
    # print(fundamentals[4].split("<br/>")[1])

    # for i in range(4, len(fundamentals)):
    #     print(fundamentals[i], end="////////////////\n")
    #     print(fundamentals[i].split('"'))

    # タグ入り全文章
    # for line in tostring(news, encoding="utf-8").decode().split():
    #     if "]" in line:
    #         print(line)
