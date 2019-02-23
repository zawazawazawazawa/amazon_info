# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_binary
from time import sleep
import pandas as pd

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

ASIN_list = ['B072L3S8GV', 'B07H7H1WJL']
info = {'商品名': {}, '商品画像': {}, '商品説明(文章)': {}, '商品説明(画像)': {}, '最低価格': {}, 'カテゴリ': {}} 

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

# ブラウザでモノレートにアクセスする
driver.get("https://mnrate.com/")

for ASIN in ASIN_list:
    sleep(2)

    # validate
    assert 'モノレート' in driver.title 

    # 検索のテキストボックス要素を取得
    element = driver.find_element_by_id("_item_search_inp")

    # テキストボックスに入力
    element.send_keys(ASIN)

    # 検索ボタンを取得
    search = driver.find_element_by_id("_graph_search_btn")

    # 検索
    search.click()

    sleep(1)
    driver.implicitly_wait(20)

    # validate
    assert driver.current_url == 'https://mnrate.com/item/aid/{}'.format(ASIN)

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main_contents > div > ul.out_site_link_list > li:nth-child(1)")))
    # 商品詳細ボタンを取得
    link = driver.find_element_by_css_selector("#main_contents > div > ul.out_site_link_list > li:nth-child(1)")

    # 商品詳細ボタンをクリック
    link.click()

    # ウィンドウハンドルを取得する(list型配列)
    handle_array = driver.window_handles

    # タブ移動
    driver.switch_to.window(handle_array[1])
    driver.implicitly_wait(20)

    # validate
    assert 'Amazon' in driver.title

    sleep(2)

    # HTMLを文字コードをUTF-8に変換してから取得します。
    html = driver.page_source.encode('utf-8')

    # BeautifulSoupで扱えるようにパースします
    soup = BeautifulSoup(html, "html.parser")

    # 商品名
    info['商品名'][ASIN] = soup.select_one("#productTitle").string.strip()

    # 商品画像(1枚)
    info['商品画像'][ASIN] = soup.select_one(".a-spacing-small.item.imageThumbnail.a-declarative img")['src'].replace('_SS40_.', '')

    # 商品説明(文章)
    description = ''
    for string in soup.select_one("#productDescription").stripped_strings:
        if string != '' and '#productDescription' not in string: # 空白行とstyleタグの中身をfiltering
            description += string
    info['商品説明(文章)'][ASIN] = description

    # 商品説明(画像)
    images =  []
    for img in soup.select("#productDescription img"):
        images.append(img['src'])
    info['商品説明(画像)'][ASIN]= images

    # 最低価格
    info['最低価格'][ASIN] = soup.select_one("#priceblock_ourprice").string

    # カテゴリ
    category_tree = ''
    for category in (soup.select("#wayfinding-breadcrumbs_feature_div > ul a")):
        category_tree += category.string.strip() + '>'
    info['カテゴリ'][ASIN] = category_tree.rstrip('>')

    driver.close()
    driver.switch_to.window(handle_array[0])

driver.quit()

result = pd.DataFrame(info)

fn = input('File name :')

# CSV ファイルとして出力
result.to_csv("{}.csv".format(fn))

print('Finish!')