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
codelists = []
for news in scraped_data:
    get_a = news.findall("a")
    print(tostring(news, encoding="utf-8").decode())
    # lxml.html.HtmlElement
    for alink in get_a:
        # print(alink.text)
        # print("https://kabutan.jp" + alink.get("href"))
        codelists.append("https://kabutan.jp" + alink.get("href"))
    # タグ入り全文章
    # for line in tostring(news, encoding="utf-8").decode().split():
    #     if "]" in line:
    #         print(line)

# 余分なやつをのける
[codelists.pop(0) for _ in range(4)]

# 銘柄のページ
for i in range(len(codelists)):
    codelist = codelists[i]
    # print(str(i) + "回目のループ→", codelist)
    r = requests.get(codelist)
    time.sleep(0.2)
    soup = BeautifulSoup(r.text, "html.parser")
    el0 = soup.select("#kobetsu_left dd")
    el = soup.select("#kobetsu_left tr")
    try:
        # 前日終値
        # print(str+int)になってますよ
        # print("始値" + chonint(el[0].select("td")[0].getText()))
        # print("高値" + chonint(el[1].select("td")[0].getText()))
        # print("安値" + chonint(el[2].select("td")[0].getText()))
        # print("終値" + chonint(el[3].select("td")[0].getText()))
        zp = chonint(el0[0].getText()[:-8])
        # zp = el0[0].getText().split('(')[0]
        op = chonint(el[0].select("td")[0].getText())
        hp = chonint(el[1].select("td")[0].getText())
        lp = chonint(el[2].select("td")[0].getText())
        ep = chonint(el[3].select("td")[0].getText())
        # hp-opが5%以上
        # if ((hp - zp) / zp) - ((op - zp) / zp) > 0.05:
        #     print(zp, op, hp)
    except Exception as e:
        print(e.message)
        pass
