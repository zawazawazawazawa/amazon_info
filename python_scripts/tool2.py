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
from selenium.common.exceptions import TimeoutException

def err_msg(col):
    print(ASIN, 'は取得できませんでした({})'.format(col))

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
print('ASINリストを貼り付けてください\n最後にfとreturnを押してください')

while True:
    input_chr = input()
    if input_chr == 'f':
        break
    else:
        ASIN_list.append(input_chr)

# 現在時刻取得、計測開始
start_time = datetime.now()
print('start', start_time.strftime("%Y/%m/%d %H:%M:%S"))

info = {'ASIN': {},'商品名': {}, '商品画像': {}, '商品説明(文章)': {}, '商品説明(画像)': {}, '最低価格': {}, 'Amazonカテゴリ': {}, 'ヤフオクカテゴリ名': {}, 'ヤフオクカテゴリID': {}} 

# カテゴリのリストを開く
category_list = pd.read_csv('category_list.csv')

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

# ブラウザでAmazonにアクセスする
counter = 0
RETRIES = 3
TIMEOUT = 10

# ページの読み込み待ち時間(10秒)
driver.set_page_load_timeout(TIMEOUT)

try:
    for ASIN in ASIN_list:
        i = 0
        while i < RETRIES:
            try:
                driver.get("https://www.amazon.co.jp/exec/obidos/ASIN/{}".format(ASIN))
                sleep(5)

            except TimeoutException:
                i = i + 1
                print("Timeout, Retrying... (%(i)s/%(max)s)" % {'i': i, 'max': RETRIES})
                continue

            else:
                break
        else:
            msg = "Page was not loaded in time(%(second)s sec)." % {'second': TIMEOUT}
            raise TimeoutException(msg)
        # try:
        #     driver.get("https://www.amazon.co.jp/exec/obidos/ASIN/{}".format(ASIN))
        #     sleep(2)
        # except TimeoutException:
        #     import traceback
        #     traceback.print_exc()
        #     print('Amazonにアクセスして表示を確認してください\n文字の入力を支持されている場合は指示に従ってください')
        #     break
        
        try:
            # validate
            assert 'Amazon' in driver.title
        except AssertionError:
            import traceback
            traceback.print_exc()
            print(ASIN, 'は無効なASINである可能性があります')
            continue

        # HTMLを文字コードをUTF-8に変換してから取得します。
        html = driver.page_source.encode('utf-8')

        # BeautifulSoupで扱えるようにパースします
        soup = BeautifulSoup(html, "html.parser")

        # 商品名 
        if soup.select_one("#productTitle") is None:
            err_msg("商品名")
            continue

        # 商品画像(1枚)
        if soup.select_one("#imgTagWrapperId > img") is None:
            err_msg("商品画像")
            continue
        
        # 商品説明(文章)
        if soup.select_one("#productDescription") is None:
            err_msg('商品説明(文章)')
            continue

        # 最低価格
        if (soup.select_one("#priceblock_ourprice") is None) and (soup.select_one("#priceblock_dealprice") is None) and (soup.select_one(".offer-price") is None):
            err_msg('最低価格')
            continue

        # Amazonカテゴリ
        if soup.select('.a-list-item > a') is False:
            err_msg('Amazonカテゴリ')
            continue

        category_tree = ''
        for category in (soup.select('.a-list-item > a')):
            if category.string:
                category_tree += category.string.strip() + '/'
        a_category = category_tree.rstrip('/')
        
        # ヤフオクカテゴリID
        large_category = a_category.split('/')[0]
        if category_list[category_list['Amazonカテゴリ名'] == large_category].empty:
            err_msg('ヤフオクカテゴリ')
            continue


        # 各要素をinfoに登録
        info['ASIN'][ASIN] = ASIN

        info['商品名'][ASIN] = soup.select_one("#productTitle").text.replace('\n', '').replace(' ', '')
        
        img_src = soup.select_one("#imgTagWrapperId > img")['src'].strip().replace('data:image/jpeg;base64,', '')
        info['商品画像'][ASIN] = img_src

        description = ''
        for string in soup.select_one("#productDescription").stripped_strings:
            if string != '' and '#productDescription' not in string: # 空白行とstyleタグの中身をfiltering
                description += string.replace(' ', '')
        info['商品説明(文章)'][ASIN] = description

        images =  []
        for img in soup.select("#productDescription img"):
            images.append(img['src'])
        info['商品説明(画像)'][ASIN]= images

        if soup.select_one("#priceblock_ourprice"):
            info['最低価格'][ASIN] = soup.select_one("#priceblock_ourprice").text.strip('￥ ,').replace(',', '') if '-' not in soup.select_one("#priceblock_ourprice").text else '999999999'
        elif soup.select_one("#priceblock_dealprice"):
            info['最低価格'][ASIN] = soup.select_one("#priceblock_dealprice").text.strip('￥ ,').replace(',', '') if '-' not in soup.select_one("#priceblock_dealprice").text else '999999999'
        elif soup.select_one(".offer-price"):
            info['最低価格'][ASIN] = soup.select_one(".offer-price").text.strip('￥ ,').replace(',', '') if '-' not in soup.select_one(".offer-price").text else '999999999'
        else:
            '999999999'
        
        info['Amazonカテゴリ'][ASIN] = a_category

        if not category_list[category_list['Amazonカテゴリ名'] == a_category].empty:
            y_category_name = category_list[category_list['Amazonカテゴリ名'] == a_category]['ヤフオクカテゴリ名'].values[0]
            y_category_id   = category_list[category_list['Amazonカテゴリ名'] == a_category]['ヤフオクカテゴリID'].values[0]
        else:
            y_category_name = category_list[category_list['Amazonカテゴリ名'] == large_category]['ヤフオクカテゴリ名'].values[0]
            y_category_id   = category_list[category_list['Amazonカテゴリ名'] == large_category]['ヤフオクカテゴリID'].values[0]
        info['ヤフオクカテゴリ名'][ASIN] = y_category_name
        info['ヤフオクカテゴリID'][ASIN] = y_category_id

        print('ASIN: ', ASIN)
        print('商品名: ', info['商品名'][ASIN])
        print('商品説明(文章): ', info['商品説明(文章)'][ASIN])
        print('最低価格: ', info['最低価格'][ASIN])
        print('Amazonカテゴリ: ', info['Amazonカテゴリ'][ASIN])
        print('ヤフオクカテゴリ名: ', info['ヤフオクカテゴリ名'][ASIN])
        print('ヤフオクカテゴリID: ', info['ヤフオクカテゴリID'][ASIN])

        counter += 1
        print(counter)
except KeyboardInterrupt:
    pass

driver.quit()

result = pd.DataFrame(info)

# 現在時刻取得、計測終了
finish_time = datetime.now()
print('finish', finish_time.strftime("%Y/%m/%d %H:%M:%S"))
print('time', finish_time - start_time)

fn = input('ファイル名を入力してください :')

# CSV ファイルとして出力
result.to_csv("{}.csv".format(fn))

print('Finish!')