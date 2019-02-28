# coding: UTF-8
import re
import pandas as pd

# URLを入力
url_list = []
print('Paste URL List\nAnd pless "f" key to finish')

while True:
    input_chr = input()
    if input_chr == 'f': # fキーで終了
        break
    else:
        url_list.append(input_chr)

asin_list = []

for url in url_list:
    for word in url.split('/'):
        if re.search('B[A-Z0-9]{9}', word):
            asin_list.append(word)

result = pd.Series(asin_list)

fn = input('File name :')

# CSV ファイルとして出力
result.to_csv("{}.csv".format(fn), index=False)

print('Finish!')