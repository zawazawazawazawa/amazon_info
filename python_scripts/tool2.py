#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_binary
from time import sleep
import pandas as pd
from datetime import datetime
import re
import os

# ブラウザのオプションを格納する変数をもらってきます。
options = Options()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
options.add_argument('--headless')

# 暫定的に必要らしい
options.add_argument('--disable-gpu')

# google-chrome-stableが動くの必要らしい
options.add_argument('--no-sandbox')

# headlessでは不要そうな機能
options.add_argument('--disable-desktop-notifications')
options.add_argument("--disable-extensions")

# UA
options.add_argument('--user-agent=hogehoge')

# 言語
options.add_argument('--lang=ja')

# 画像を読み込まないで軽くする
options.add_argument('--blink-settings=imagesEnabled=false')

# ASINを入力
ASIN_list = []
print('Paste ASIN List\nAnd pless "f" key to finish')

while True:
    input_chr = input()
    if input_chr == 'f':
        break
    else:
        ASIN_list.append(input_chr)

# 現在時刻取得、計測開始
start_time = datetime.now()
print('start', start_time.strftime("%Y/%m/%d %H:%M:%S"))

info = {'ASIN': {},'商品名': {}, '商品画像': {}, '商品説明(文章)': {}, '商品説明(画像)': {}, '最低価格': {}, 'Amazonカテゴリ': {}, 'ヤフオクカテゴリ': {}} 

# カテゴリのリストを開く
category_list = pd.read_csv('python_scripts/category_list.csv')

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

# ブラウザでAmazonにアクセスする
counter = 0
for ASIN in ASIN_list:
    driver.get("https://www.amazon.co.jp/exec/obidos/ASIN/{}".format(ASIN))
    sleep(2)

    # validate
    assert 'Amazon' in driver.title

    # HTMLを文字コードをUTF-8に変換してから取得します。
    html = driver.page_source.encode('utf-8')

    # BeautifulSoupで扱えるようにパースします
    soup = BeautifulSoup(html, "html.parser")

    # ASIN
    info['ASIN'] = ASIN

    # 商品名
    info['商品名'][ASIN] = soup.select_one("#productTitle").string.strip() if soup.select_one("#productTitle") is not None else ''

    # 商品画像(1枚)
    image_url = soup.select_one(".a-spacing-small.item.imageThumbnail.a-declarative img")['src'] if soup.select_one(".a-spacing-small.item.imageThumbnail.a-declarative img") is not None else ''
    info['商品画像'][ASIN] = re.sub('\._[a-zA-Z0-9_,]*_\.', '.', image_url)

    # 商品説明(文章)
    description = ''
    if soup.select_one("#productDescription") is not None:
        for string in soup.select_one("#productDescription").stripped_strings:
            if string != '' and '#productDescription' not in string: # 空白行とstyleタグの中身をfiltering
                description += string.replace(' ', '')
        info['商品説明(文章)'][ASIN] = description
    else:
        info['商品説明(文章)'][ASIN] = ''

    # 商品説明(画像)
    images =  []
    if soup.select("#productDescription img") is not None:
        for img in soup.select("#productDescription img"):
            images.append(img['src'])
        info['商品説明(画像)'][ASIN]= images
    else:
        info['商品説明(画像)'][ASIN]= ''

    # 最低価格
    if soup.select_one("#priceblock_ourprice") is not None:
        info['最低価格'][ASIN] = soup.select_one("#priceblock_ourprice").string.strip('￥ ,').replace(',', '') if '-' not in soup.select_one("#priceblock_ourprice").string else '999999999'
    elif soup.select_one("#priceblock_dealprice") is not None:
        info['最低価格'][ASIN] = soup.select_one("#priceblock_dealprice").string.strip('￥ ,').replace(',', '') if '-' not in soup.select_one("#priceblock_dealprice").string else '999999999'
    else:
        info['最低価格'][ASIN] = '999999999'

    # Amazonカテゴリ
    category_tree = ''
    if soup.select("#wayfinding-breadcrumbs_feature_div > ul a") is not None:
        for category in (soup.select("#wayfinding-breadcrumbs_feature_div > ul a")):
            category_tree += category.string.strip() + '/'
        a_category = category_tree.rstrip('/')
    else:
        a_category = ''
    info['Amazonカテゴリ'][ASIN] = a_category
    
    # ヤフオクカテゴリ
    if a_category == '':
        y_category = ''
    else:
        y_category = category_list[category_list['Amazonカテゴリ名'] == a_category]['ヤフオクカテゴリID'].values[0]
    info['ヤフオクカテゴリ'][ASIN] = y_category



    counter += 1
    print(counter)

driver.quit()

result = pd.DataFrame(info)

# 現在時刻取得、計測終了
finish_time = datetime.now()
print('finish', finish_time.strftime("%Y/%m/%d %H:%M:%S"))
print('time', finish_time - start_time)

fn = input('File name :')

# CSV ファイルとして出力
result.to_csv("{}.csv".format(fn))

print('Finish!')