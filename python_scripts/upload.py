from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import chromedriver_binary
from time import sleep
import os

# ブラウザのオプションを格納する変数をもらってきます。
options = Options()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
# options.add_argument('--headless')

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

# ユーザー名とパスワードとzipファイル名をターミナルに入力
username = input('Username?: ')
password = input('Password?: ')
fn = input('Filename?: ')

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

driver.get('http://auctown.jp/')
sleep(2)

# ログインボタンをクリック
driver.find_element_by_css_selector('#header > div.topmenu > a').click()
sleep(2)

# ユーザー名を入力
driver.find_element_by_id('username').send_keys(username)
driver.find_element_by_id('btnNext').click()
sleep(2)

# passwordを入力
driver.find_element_by_id('passwd').send_keys(password)
driver.find_element_by_id('btnSubmit').click()
sleep(2)

# 一括商品登録へ
driver.get('https://auctown.jp/bulkUploadStep1/')
sleep(2)

# ファイルをアップロード
driver.find_element_by_css_selector('#zipFrm > table > tbody > tr > td > input[type="file"]').send_keys(os.path.abspath('{}.zip'.format(fn)))
driver.find_element_by_id('zipSend').click()
sleep(2)

# いますぐアップロード
driver.find_element_by_id('bulkNowSubmit').click()
sleep(2)
Alert(driver).accept()

# HTMLを文字コードをUTF-8に変換してから取得します。
html = driver.page_source.encode('utf-8')

# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")

# driver.quit()