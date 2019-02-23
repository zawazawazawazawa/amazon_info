# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_binary
from time import sleep

ASIN     = 'B072L3S8GV'
info = {'商品名': {}, '商品画像': {}, '商品説明': {}, '最低価格': {}, 'カテゴリ': {}} 

# ブラウザのオプションを格納する変数をもらってきます。
options = Options()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
options.add_argument('--headless')

# 暫定的に必要らしい
options.add_argument('--disable-gpu')

# google-chrome-stableが動くの必要らしい
options.add_argument('--no-sandbox')

# エラーの許容
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-running-insecure-content')
# options.add_argument('--disable-web-security')

# headlessでは不要そうな機能
options.add_argument('--disable-desktop-notifications')
options.add_argument("--disable-extensions")

# UA
options.add_argument('--user-agent=hogehoge')

# 言語
options.add_argument('--lang=ja')

# 画像を読み込まないで軽くする
options.add_argument('--blink-settings=imagesEnabled=false')

capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptInsecureCerts'] = True

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capabilities)

driver.implicitly_wait(20)

# ブラウザでモノレートにアクセスする
driver.get("https://mnrate.com/")

sleep(1)

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
assert "アタックNeo 抗菌EX Wパワー 洗濯洗剤 濃縮液体 詰替用 1300g" in driver.title

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

# HTMLを文字コードをUTF-8に変換してから取得します。
html = driver.page_source.encode('utf-8')

# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")

# 商品名
info['商品名'][ASIN] = soup.select_one("#productTitle").string.strip()

# 商品画像(1枚)
info['商品画像'][ASIN] = str(soup.select_one(".a-spacing-small.item.imageThumbnail.a-declarative img"))[10:-3].replace('_SS40_.', '')

# 商品説明
description = ''
for string in soup.select_one("#productDescription").strings:
    if string.strip() != '':
        description += string.strip()
info['商品説明'] = description

# 最低価格
info['最低価格'] = soup.select_one("#priceblock_ourprice").string

# カテゴリ
category_tree = ''
for category in (soup.select("#wayfinding-breadcrumbs_feature_div > ul a")):
    category_tree += category.string.strip() + '>'
info['カテゴリ'] = category_tree.rstrip('>')

print(info)

driver.quit()


# # 商品画像
# print('商品画像')
# for image in soup.select(".a-spacing-small.item.imageThumbnail.a-declarative"):
#     print(str(image.select_one("img"))[10:-3].replace('_SS40_.', ''))