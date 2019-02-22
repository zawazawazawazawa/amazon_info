# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from time import sleep

# ブラウザのオプションを格納する変数をもらってきます。
options = Options()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
options.set_headless(True)

# ブラウザを起動する
driver = webdriver.Chrome(options=options)

# ブラウザでアクセスする
driver.get("https://www.amazon.co.jp/exec/obidos/ASIN/B072L3S8GV")

sleep(1)

# HTMLを文字コードをUTF-8に変換してから取得します。
html = driver.page_source.encode('utf-8')

# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")

# 商品名
# print('商品名', soup.select_one("#productTitle").string.strip())

# 商品画像
# for image in soup.select(".a-spacing-small.item.imageThumbnail.a-declarative"):
#     print('商品画像', str(image.select_one("img"))[10:-3].replace('_SS40_.', ''))

# 商品説明
# for string in soup.select_one("#productDescription").strings:
#     if string.strip() != '':
#         print(string.strip())

# 最低価格
# print(soup.select_one("#priceblock_ourprice").string[2:])

# カテゴリ
for category in (soup.select_one("#SalesRank .zg_hrsr_ladder")):
    print(category)
