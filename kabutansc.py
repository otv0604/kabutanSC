import time
import datetime
import requests
from bs4 import BeautifulSoup
from lxml.etree import tostring
import lxml.html
import openpyxl as ol

# 株価整形関数
def Str2Int(num):
    n = num.replace(",", "")
    return float(n)


# 注目ニュース一覧ページ
url = "https://kabutan.jp/news/marketnews/?category=9"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

# 今朝の注目ニュースを抽出
for element in soup.find_all("a"):
    # テキストに「今朝」が含まれているか調べる
    if "今朝" in element.text:
        link = element.get("href")

# 今朝の注目ニュースページ
url = "https://kabutan.jp" + link
req = requests.get(url)
html = req.text
dom = lxml.html.fromstring(html)

# div class='body'のxpathを取得
target_xpath = '//*[@id="shijyounews"]/article/div'
scraped_data = dom.xpath(target_xpath)

# 銘柄名、URL、材料を取得
meigaralists, codelists, descriptions = [], [], []
for news in scraped_data:
    articles = tostring(news, encoding="utf-8").decode().replace("\n", "")
    # 7行目から3step毎の各情報を取得する
    for i, codelist in enumerate(articles.split("<br/>")[7:]):
        # 現状悪材料以下は取得しない設定となっている
        if "【悪材料】" in codelist:
            break
        elif i % 3 == 0:
            # 銘柄名一覧
            meigaralists.append(codelist.split()[0])
            # コードURL一覧
            codelists.append("https://kabutan.jp" + codelist.split('"')[1])
        elif i % 3 == 1:
            # 材料一覧
            descriptions.append(codelist.split()[0])

# 個別銘柄ページ
for i in range(len(codelists)):
    url = codelists[i]
    req = requests.get(url)
    time.sleep(0.2)
    soup = BeautifulSoup(req.text, "html.parser")
    # 銘柄名抽出
    meigara = soup.select("#kobetsu_left dd")
    # 株価抽出
    price = soup.select("#kobetsu_left tr")
    try:
        yesterdayowarine = Str2Int(meigara[0].getText()[:-8])
        openprice = Str2Int(price[0].select("td")[0].getText())
        highprice = Str2Int(price[1].select("td")[0].getText())
        lowprice = Str2Int(price[2].select("td")[0].getText())
        endprice = Str2Int(price[3].select("td")[0].getText())
        # 始値から5%以上あがった銘柄のみを抽出
        if ((highprice - yesterdayowarine) / yesterdayowarine) - (
            (openprice - yesterdayowarine) / yesterdayowarine
        ) > 0.05:
            # excelに保存
            wb = ol.load_workbook("D:\Down/kabutan.xlsx")
            # zshから実行する場合のファイルパス
            # wb = ol.load_workbook("/mnt/d/Down/kabutan.xlsx")
            ws = wb["Sheet1"]
            max_row = ws.max_row + 1
            print(max_row)
            ws.cell(row=max_row, column=1).value = datetime.datetime.now()
            ws.cell(row=max_row, column=2).value = str(meigaralists[i])
            ws.cell(row=max_row, column=3).value = int(yesterdayowarine)
            ws.cell(row=max_row, column=4).value = int(openprice)
            ws.cell(row=max_row, column=5).value = int(highprice)
            ws.cell(row=max_row, column=6).value = int(lowprice)
            ws.cell(row=max_row, column=7).value = int(endprice)
            ws.cell(row=max_row, column=8).value = str(descriptions[i])
            wb.save("D:\Down/kabutan.xlsx")
            # zshから実行する場合のファイルパス
            # wb.save("/mnt/d/Down/kabutan.xlsx")
    # 例外処理
    except Exception as e:
        print(e.message)
        pass
