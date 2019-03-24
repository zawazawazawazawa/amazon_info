# coding: UTF-8
import re
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_binary
from time import sleep
from datetime import datetime
import os

def get_asin(url):
    driver.get(url)
    sleep(2)

    # validate
    assert 'Amazon' in driver.title

    # HTMLを文字コードをUTF-8に変換してから取得します。
    html = driver.page_source.encode('utf-8')

    # BeautifulSoupで扱えるようにパースします
    soup = BeautifulSoup(html, "html.parser")

    li_elements = soup.find_all(attrs = {'data-asin':True})
    for li_element in li_elements:
        asin = li_element['data-asin']
        asin_list.append(asin)

    if soup.select_one('#pagnNextLink') and len(asin_list) < max:
        nextUrl = soup.select_one('#pagnNextLink')['href']
        get_asin(domain+nextUrl)

# URLを入力
url = input('検索結果のURLを入力してください: ')

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

# 取得する数を入力
max = int(input('取得する商品数を入力してください: '))
asin_list = []
domain = 'https://www.amazon.co.jp'

# 現在時刻取得、計測開始
start_time = datetime.now()
print('start', start_time.strftime("%Y/%m/%d %H:%M:%S"))

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

get_asin(url)
driver.quit()

result = pd.Series(asin_list[:max])

fn = input('ファイル名を入力してください :')

# CSV ファイルとして出力
result.to_csv("{}.csv".format(fn), index=False)

print('Finish!')