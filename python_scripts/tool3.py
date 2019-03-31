import pandas as pd
import copy
import requests
import os
import zipfile
import shutil
import cv2
import base64
import numpy as np
import io

def description(title, description):
    description = ('<center>'
                    '  <font color="#666666" size="4"><b bgcolor="#FFE566" align="center">'
                    '  {}</b></font><br>'
                    '  <br>'
                    '  <table width="600" cellpadding="10">'
                    '  <tbody>'
                    '  <tr>'
                    '    <td bgcolor="#FFFFFF">'
                    '      <table width="100%" cellspacing="0" border="0" cellpadding="0">'
                    '      <tbody>'
                    '      <tr>'
                    '        <td bgcolor="#FFCC33" valign="top" height="32">'
                    '          <table width="100%" cellspacing="0" border="0" cellpadding="0">'
                    '          <tbody>'
                    '          <tr>'
                    '            <td bgcolor="#FFE566" align="center" height="30" width="25%">'
                    '              <font color="#000000" size="3"><b>'
                    '              商品詳細'
                    '              </b></font>'
                    '            </td>'
                    '            <td bgcolor="#FFFFFF" width="75%">'
                    '            </td>'
                    '          </tr>'
                    '          </tbody>'
                    '          </table>'
                    '        </td>'
                    '      </tr>'
                    '      <tr>'
                    '        <td>'
                    '          <table cellspacing="15" width="100%">'
                    '          <tbody>'
                    '          <tr>'
                    '            <td align="left">'
                    '              <font size="2" color="#000000">'
                    '             {}</font>'
                    '            </td>'
                    '          </tr>'
                    '          </tbody>'
                    '          </table>'
                    '        </td>'
                    '      </tr>'
                    '      </tbody>'
                    '      </table>'
                    '      <table width="100%" cellspacing="0" border="0" cellpadding="0">'
                    '      <tbody>'
                    '      <tr>'
                    '        <td bgcolor="#FFCC33" valign="top" height="32">'
                    '          <table width="100%" cellspacing="0" border="0" cellpadding="0">'
                    '          <tbody>'
                    '          <tr>'
                    '            <td bgcolor="#FFE566" align="center" height="30" width="25%">'
                    '              <font color="#000000" size="3"><b>'
                    '              支払詳細'
                    '              </b></font>'
                    '            </td>'
                    '            <td bgcolor="#FFFFFF" width="75%">'
                    '            </td>'
                    '          </tr>'
                    '          </tbody>'
                    '          </table>'
                    '        </td>'
                    '      </tr>'
                    '      <tr>'
                    '        <td>'
                    '          <table cellspacing="15" width="100%">'
                    '          <tbody>'
                    '          <tr>'
                    '            <td align="left">'
                    '              <font size="2" color="#000000">'
                    '              お支払い方法　：　Yahoo!かんたん決済<br>'
                    '              <br>'
                    '              <b>【落札代金】＋【送料】＝【お支払い代金】</b><br>'
                    '              <br>'
                    '              ※お振込手数料等はご負担下さい。<br>'
                    '              <br>'
                    '              ※領収書発行は受け付けておりません。<br>'
                    '              <br>'
                    '              </font>'
                    '            </td>'
                    '          </tr>'
                    '          </tbody>'
                    '          </table>'
                    '        </td>'
                    '      </tr>'
                    '      </tbody>'
                    '      </table>'
                    '      <table width="100%" cellspacing="0" border="0" cellpadding="0">'
                    '      <tbody>'
                    '      <tr>'
                    '        <td bgcolor="#FFCC33" valign="top" height="32">'
                    '          <table width="100%" cellspacing="0" border="0" cellpadding="0">'
                    '          <tbody>'
                    '          <tr>'
                    '            <td bgcolor="#FFE566" align="center" height="30" width="25%">'
                    '              <font color="#000000" size="3"><b>'
                    '              発送詳細'
                    '              </b></font>'
                    '            </td>'
                    '            <td bgcolor="#FFFFFF" width="75%">'
                    '            </td>'
                    '          </tr>'
                    '          </tbody>'
                    '          </table>'
                    '        </td>'
                    '      </tr>'
                    '      <tr>'
                    '        <td>'
                    '          <table cellspacing="15" width="100%">'
                    '          <tbody>'
                    '          <tr>'
                    '            <td align="left">'
                    '              <font size="2" color="#000000"><br>'
                    '              全国一律　送料500円<br>'
                    '              ※複数個同時に落札していただいた場合も、個別の送料がかかります。<br>'
                    '              倉庫配送システムの関係で同梱でも 送料は原則個数分頂戴いたします。<br>'
                    '              <br>'
                    '              ※局留め、営業所止め、コンビニ受け取り、代金引換払いはできません。<br>'
                    '              <br>'
                    '              ※全国一律の配送料金契約をしており、倉庫からの集荷配送を提携業者から最善の方法を選択してお届けしております為、配送業者のご指定、および配送日時指定をお受けする事は出来ません。<br>'
                    '              <br>'
                    '              ※環境に配慮して、段ボールの再利用をしております為、無地以外のパッケージで商品が届く場合がございます。<br>'
                    '              <br>'
                    '              以上ご了承頂いたうえで、入札をお願い致します。<br>'
                    '              </font>'
                    '            </td>'
                    '          </tr>'
                    '          </tbody>'
                    '          </table>'
                    '        </td>'
                    '      </tr>'
                    '      </tbody>'
                    '      </table>'
                    '      <table width="100%" cellspacing="0" border="0" cellpadding="0">'
                    '      <tbody>'
                    '      <tr>'
                    '        <td bgcolor="#FFCC33" valign="top" height="32">'
                    '          <table width="100%" cellspacing="0" border="0" cellpadding="0">'
                    '          <tbody>'
                    '          <tr>'
                    '            <td bgcolor="#FFE566" align="center" height="30" width="25%">'
                    '              <font color="#000000" size="3"><b>'
                    '              注意事項'
                    '              </b></font>'
                    '            </td>'
                    '            <td bgcolor="#FFFFFF" width="75%">'
                    '            </td>'
                    '          </tr>'
                    '          </tbody>'
                    '          </table>'
                    '        </td>'
                    '      </tr>'
                    '      <tr>'
                    '        <td>'
                    '          <table cellspacing="15" width="100%">'
                    '          <tbody>'
                    '          <tr>'
                    '            <td align="left">'
                    '              <font color="#000000"><font size="2">'
                    '              <br>'
                    '              ・落札後５日を過ぎてもご連絡が無い場合は お客様都合でのキャンセル扱いとさせて頂きます。<br>'
                    '              　その際、ヤフオクシステムにより、自動的に落札者様のマイナス評価となりますこと、予めご了承ください。<br><br>'
                    '              ・落札後に落札者様のご都合によるキャンセルは出品者の金銭的負担が発生するためお受けする事はできません。<br><br>'
                    '              ・新規IDの方・悪い評価が多い方は、予告無く入札を削除する場合があります。<br>（落札後のキャンセルや連絡が無いなどの取引トラブル防止の為、ご了承ください。）<br><br>'
                    '              ・商品によっては説明書が中国語や英語で記載されている場合がございます。予めご了承ください。<br>'
                    '              ・ヤフオクのシステム上、複数個数の出品の際に、詳細情報に複数個数表示されますが、入札件数とは異なりますのでご注意ください。<br>'
                    '              複数個数ご希望の場合は、ご希望個数を入力してご入札されてください。<br><br>'
                    '              ・商品により発送を委託する場合があります。<br>'
                    '              その場合は取引ナビにてご入力された氏名や住所などの個人情報は、<br>'
                    '              落札商品をお届けするために必要な範囲で配送業者などの第三者に通知させて頂きます。<br><br>'
                    '              ・在庫管理は徹底しておりますが、稀に商品が行き違いにて在庫切れとなる場合もございます。<br>'
                    '              その際は大変申し訳ございませんが、ご注文はキ ャンセルさせて頂き、ご返金となりますこと、予めご了承ください。<br>'
                    '              以上ご了承頂いたうえで、入札をお願い致します。'
                    '              </font>'
                    '            </td>'
                    '          </tr>'
                    '          </tbody>'
                    '          </table>'
                    '        </td>'
                    '      </tr>'
                    '      </tbody>'
                    '      </table>'
                    '    </td>'
                    '  </tr>'
                    '  </tbody>'
                    '  </table>'
                    '  <br>'
                    '  <font color="#999999" size="1">+ + +　この商品説明は</font><a href="http://www.auclinks.com/" target="new"><font color="#666666" size="1">オークションプレートメーカー２</font></a><font color="#999999" size="1">で作成しました 　+ + +</font><font color="#FFFFFF" size="1"><br>'
                    '  No.204.001.002'
                    '  </font><br>'
                    '</center>'.format(title, description))
    return description
                    

templete = {
    # 必須:○
    'カテゴリ': '', #半角数字, ○
    'タイトル': '', #全角30文字以内, ○
    '説明'   : '', #全角25000文字以内, ○
    '開始価格': '', #数値, ○
    '即決価格': '', #数値
    '個数'   : '1', #1−9, ○
    '開催期間': '2', #2−7, ○
    '終了時間': '22', #0−23, ○
    '画像1': '', #半角英数ファイル名
    '画像2': '',
    '画像3': '',
    '画像4': '',
    '画像5': '',
    '画像6': '',
    '画像7': '',
    '画像8': '',
    '画像9': '',
    '画像10': '',
    '商品発送元の都道府県': '東京都', #都道府県名, ○
    '送料負担': '落札者', #落札者OR出品者, ○
    '代金支払い': '先払い', #先払いOR後払い, ○
    'yahoo!簡単決済': 'はい', #はいORいいえ, ○
    'かんたん取引': 'はい', #はいORいいえ
    '商品代引': 'いいえ', #はいORいいえ
    '商品の状態': '新品', #新品、未使用に近い、目立った傷や汚れなし、
                    #やや傷や汚れあり、傷や汚れあり、全体的に状態が悪い、
                    #中古、その他 ○
    '返品の可否': '返品不可', #返品不可、返品可、○
    '入札者評価制限': 'いいえ', #はいORいいえ
    '悪い評価の割合で制限': 'いいえ', #はいORいいえ
    '入札者認証制限': 'いいえ', #はいORいいえ
    '自動延長': 'はい', #はいORいいえ
    '早期終了': 'はい', #はいORいいえ
    '値下げ交渉': 'いいえ', #はいORいいえ
    '自動再出品': '3', #0～3の数値
    '自動値下げ': 'いいえ', #はいORいいえ
    '太字テキスト': 'いいえ', #はいORいいえ
    '背景色': 'いいえ', #はいORいいえ
    '贈答品アイコン': 'いいえ', #はいORいいえ
    '送料固定': 'はい', #はいORいいえOR着払い
    'ネコポス': 'いいえ', #はいORいいえ
    'ネコ宅急便コンパクト': 'いいえ', #はいORいいえ
    'ネコ宅急便': 'いいえ', #はいORいいえ
    'ゆうパケット': 'いいえ', #はいORいいえ
    'ゆうパック': 'いいえ', #はいORいいえ
    '発送までの日数': '3日～6日', #1日～2日、3日～6日、7日～13日、14日以降
    '配送方法1': '宅急便（ヤマト運輸）', #全角15文字以内、10件まで
    '配送方法1全国一律価格': '500', #半角英数字
    '海外発送': 'いいえ', #はいORいいえ
    'アフィリエイト': 'はい', #はいORいいえ
    '出品者情報開示前チェック': 'いいえ' #はいORいいえ
}

#ディレクトリの初期化
if os.path.isdir('upload_files'):
    shutil.rmtree('upload_files')
os.mkdir('upload_files')

# csvファイル名
csv_file = input('CSVファイルの名前を入力してください: ') + '.csv'

# 発送までの日数
days = input('発送までの日数を\n1日～2日、3日～6日、7日～13日、14日以降\nから選んでください: ')

# アフィリエイト
af = input('アフィリエイトをはい又はいいえで選んでください: ')

# 開催期間
op = int(input('開催期間を2−7で入力してください: '))

# 終了時間
ft = int(input('終了時間を0-23で選んでください: '))

# 送料
postage = int(input('送料を入力してください: '))

# 最低価格の割合
lp = float(input('最低価格の割合を入力してください: '))

# 即決価格の割合
dp = float(input('即決価格の割合を入力してください: '))


# amazonの商品情報リストを開く
amazon_list = pd.read_csv(csv_file)

# 出力用の辞書を用意
result = []

for n in range(len(amazon_list.index)):
    try:
        new_templete = copy.deepcopy(templete)

        assert amazon_list.loc[n]['ヤフオクカテゴリID'] == amazon_list.loc[n]['ヤフオクカテゴリID']
        new_templete['カテゴリID'] = int(amazon_list.loc[n]['ヤフオクカテゴリID'])

        assert amazon_list.loc[n]['ヤフオクカテゴリ名'] == amazon_list.loc[n]['ヤフオクカテゴリ名']
        new_templete['カテゴリ名'] = amazon_list.loc[n]['ヤフオクカテゴリ名']

        assert amazon_list.loc[n]['商品名'] == amazon_list.loc[n]['商品名']
        new_templete['タイトル'] = amazon_list.loc[n]['商品名'][:63] 

        assert amazon_list.loc[n]['商品説明(文章)'] == amazon_list.loc[n]['商品説明(文章)']
        new_templete['説明'] = description(amazon_list.loc[n]['商品名'], amazon_list.loc[n]['商品説明(文章)']) 

        assert amazon_list.loc[n]['最低価格'] == amazon_list.loc[n]['最低価格']
        new_templete['開始価格'] = int(round(int(amazon_list.loc[n]['最低価格']) * lp, 0)) 
        new_templete['即決価格'] = int(round(int(amazon_list.loc[n]['最低価格']) * dp, 0))

        #画像保存先
        image_file=r"upload_files/{}.jpg".format(n)
        img_base64 = amazon_list.loc[n]['商品画像']

        #バイナリデータ <- base64でエンコードされたデータ  
        img_binary = base64.b64decode(img_base64)
        jpg=np.frombuffer(img_binary,dtype=np.uint8)

        #raw image <- jpg
        img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)

        height = img.shape[0]
        width  = img.shape[1]

        if width / height > 2.5:
            size = (height*4, height*2)
            img = cv2.resize(img, size)

        #画像を保存する場合
        cv2.imwrite(image_file,img)

        new_templete['画像1'] = '{}.jpg'.format(n)

        result.append(new_templete)

        new_templete['発送までの日数'] = days
        new_templete['アフィリエイト'] = af
        new_templete['開催期間'] = op
        new_templete['終了時間'] = ft
        new_templete['配送方法1全国一律価格'] = postage
    
    except:
        import traceback
        traceback.print_exc()
        print(amazon_list.loc[n]['ASIN'], 'は出品できません')
        continue 
                                                
df = pd.DataFrame(result)

# CSV ファイルとして出力
df.to_csv("upload_files/data.csv")

# fn = input('zipファイルの名前を入力してください:')

# shutil.make_archive(fn, 'zip', 'upload_files')

print('Finish!')
