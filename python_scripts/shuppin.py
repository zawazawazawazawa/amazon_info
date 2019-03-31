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
import datetime
import re
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select

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

# ユーザー名
username = input('ユーザー名を入力してください: ')

# パスワード
passwd = input('パスワードを入力してください: ')

# csvファイル名
fn = 'upload_files/data.csv'

# 現在時刻取得、計測開始
start_time = datetime.datetime.now()
print('start', start_time.strftime("%Y/%m/%d %H:%M:%S"))

# csvファイルを開く
df = pd.read_csv(fn).T

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

# 出品へ移動
driver.get('https://auctions.yahoo.co.jp/sell/jp/show/topsubmit?category=0')

if 'ログイン' in driver.title:
    # ユーザー名入力
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('btnNext').click()
    sleep(2)

    # パスワード入力
    driver.find_element_by_id('passwd').send_keys(passwd)
    driver.find_element_by_id('btnSubmit').click()
    sleep(2)

for n in range(len(df.columns)):
    driver.get('https://auctions.yahoo.co.jp/sell/jp/show/topsubmit?category=0')
    sleep(2)

    # カテゴリ検索
    driver.find_element_by_css_selector('#CategorySelect > ul > li:nth-child(2) > a > div').click()
    driver.find_element_by_id('category-search-keyword').send_keys(df[n]['カテゴリ名'].replace('オークション', '').replace(' > ', ' '))
    driver.find_element_by_css_selector('#CategorySelect > div:nth-child(3) > div.SearchBox > form > span.Button.Button--search > input').click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_category_index1")))

    # 一番上をチェック
    driver.find_element_by_id('search_category_index1').click()
    driver.find_element_by_id('search_category_submit').click()
    sleep(2)


    # 商品名
    driver.find_element_by_id('auc_title').send_keys(df[n]['タイトル'])

    # 説明
    driver.find_element_by_css_selector('#textMode > div.decFormTab > table > tbody > tr > td.decFormTab01On').click()
    driver.find_element_by_css_selector('#textMode > div.decFormTxtArea > textarea:nth-child(1)').send_keys(df[n]['説明'])

    # 販売形式
    driver.find_element_by_id('salesmode_auction').click()

    # 開始価格
    driver.find_element_by_id('auc_StartPrice').send_keys(df[n]['開始価格'])

    # 即決価格
    driver.find_element_by_id('auc_BidOrBuyPrice').send_keys(df[n]['即決価格'])

    # 開催期間
    today = datetime.date.today()
    op = df[n]['開催期間']
    fd = (today + datetime.timedelta(op)).strftime("%Y-%m-%d")

    closingDate = driver.find_element_by_id('ClosingYMD')
    Select(closingDate).select_by_value(fd)

    # 終了時間
    closingTime = driver.find_element_by_id('ClosingTime')
    ft = str(df[n]['終了時間'])
    Select(closingTime).select_by_value(ft)

    # 発送元の地域:東京
    loc = driver.find_element_by_id('auc_loc_cd')
    Select(loc).select_by_value('13')

    # 送料負担:落札者
    driver.find_element_by_id('auc_shipping_buyer').click()

    # 配送方法
    # 出品時に送料を入力
    driver.find_element_by_id('auc_shipping_fixed').click()

    # その他の配送サービス、チェック
    if not driver.find_element_by_id('shipping_other').is_selected():
        driver.find_element_by_id('shipping_other').click()

    delivery = driver.find_element_by_id('auc_shipname_standard1')
    Select(delivery).select_by_value('宅急便（ヤマト運輸）')

    driver.find_element_by_id('auc_shipname_uniform_fee_data1').clear()
    driver.find_element_by_id('auc_shipname_uniform_fee_data1').send_keys(df[n]['配送方法1全国一律価格'])

    # 発送までの日数
    if df[n]['発送までの日数'] == '1日～2日':
        driver.find_element_by_css_selector('#shipping1').click()
    elif df[n]['発送までの日数'] == '3日～6日':
        driver.find_element_by_css_selector('#shipping4').click()
    elif df[n]['発送までの日数'] == '7日～13日':
        driver.find_element_by_css_selector('#shipping5').click()
    else:
        driver.find_element_by_css_selector('#shipping6').click()

    # 商品の状態:新品、未使用
    driver.find_element_by_id('istatus_new').click()

    # 返品の可否:返品不可
    driver.find_element_by_id('retpolicy_no').click()

    # 商品画像
    driver.find_element_by_css_selector('#ImageUpArea > div.MoveImageUpTool > a').click()
    sleep(2)

    driver.find_element_by_css_selector('#upform > div > table > tbody > tr:nth-child(1) > td > input').send_keys(os.path.abspath('upload_files/{}'.format(df[n]['画像1'])))
    driver.find_element_by_css_selector('#js-confirm-button').click()
    driver.find_element_by_css_selector('#back_btn').click()

    # みんなのチャリティー:いいえ
    driver.find_element_by_css_selector('#charopt_0').click

    # 入札者評価制限:いいえ
    if driver.find_element_by_css_selector('#auc_minBidRating').is_selected():
        driver.find_element_by_css_selector('#auc_minBidRating').click()

    if driver.find_element_by_css_selector('#auc_badRatingRatio').is_selected():
        driver.find_element_by_css_selector('#auc_badRatingRatio').click()

    # 入札者認証制限:いいえ
    if driver.find_element_by_css_selector('#bidCreditLimit').is_selected():
        driver.find_element_by_css_selector('#bidCreditLimit').click()

    # 自動延長:はい
    if not driver.find_element_by_css_selector('#auc_AutoExtension').is_selected():
        driver.find_element_by_css_selector('#auc_AutoExtension').click()

    # 早期終了:はい
    if not driver.find_element_by_css_selector('#auc_CloseEarly').is_selected():
        driver.find_element_by_css_selector('#auc_CloseEarly').click()

    # 自動再出品:3
    reSubmit = driver.find_element_by_css_selector('#numResubmit')
    Select(reSubmit).select_by_value('3')

    # 自動値下げ:いいえ
    if driver.find_element_by_css_selector('#auc_AutoSell').is_selected():
        driver.find_element_by_css_selector('#auc_AutoSell').click()

    # 出品者情報開示前チェック:いいえ
    if driver.find_element_by_css_selector('#auc_SalesContract').is_selected():
        driver.find_element_by_css_selector('#auc_SalesContract').click()

    # アフィリエイト
    if df[n]['アフィリエイト'] == 'はい':
        if driver.find_element_by_css_selector('#auc_affiliate').is_selected():
            pass
        else:
            driver.find_element_by_css_selector('#auc_affiliate').click()
    else:
        if driver.find_element_by_css_selector('#auc_affiliate').is_selected():
            driver.find_element_by_css_selector('#auc_affiliate').click()
        else:
            pass

    # 確認画面へ
    driver.find_element_by_id('auc_submit1').click()
    sleep(2)

    # 出品
    driver.find_element_by_css_selector('#auc_preview_submit_up').click()

    print(n + 1)

    # 下書きに保存
    # driver.find_element_by_css_selector('#auc_preview_draft_up').click()