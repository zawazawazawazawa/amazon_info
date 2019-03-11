#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import chromedriver_binary


th_objs = [] # スレッドの配列
driver = {}  # 各スレッドのwebdriverオブジェクト格納用

# ブラウザのサイズと表示位置
browsers = [
    { "size-x": "700", "size-y": "700", "pos-x": "0",    "pos-y": "0"},
    { "size-x": "700", "size-y": "700", "pos-x": "800",  "pos-y": "0"}
]

# アクセスするウェブサイト
sites =  [
    { "www": "http://www.amazon.co.jp"    },
    { "www": "http://www.google.com"      },
    { "www": "http://www.yahoo.com"       },
    { "www": "http://www.ibm.com"         },
    { "www": "http://www.yahoo.co.jp"     },
    { "www": "http://qiita.com/MahoTakara"}
]


# スレッドでブラウザを制御する関数
def proc(idx):
    browser = browsers[idx]
    tid = threading.get_ident()

    # ブラウザを択一
    driver[tid] = webdriver.Chrome()
    # driver[tid] = webdriver.Firefox()

    # 位置とサイズ指定
    driver[tid].set_window_size(browser['size-x'], browser['size-y'])
    driver[tid].set_window_position(browser['pos-x'], browser['pos-y'])

    # サイトを巡回
    for site in sites:
        print("idx: ", idx, "id:", threading.get_ident(), "title: ", driver[tid].title)
        driver[tid].get(site['www'])
        time.sleep(3)

    # 終了
    driver[tid].quit()        


# メイン
if __name__ == '__main__':

    # スレッドを登録
    for idx in range(0,len(browsers)):
        th_objs.append( threading.Thread( target=proc,args=(idx,)))

    # スレッドの実行開始
    for i in range(0,len(browsers)):
        th_objs[i].start()