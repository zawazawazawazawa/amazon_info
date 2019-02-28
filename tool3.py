import pandas as pd

category = pd.read_csv('ChangeCategory.csv')

a_categories = ['家電＆カメラ/カメラ/アクセサリ/ウェアラブルカメラ用アクセサリ/ウェアラブルカメラ用マウント部品','家電＆カメラ/携帯電話・スマートフォン/携帯電話・スマートフォンアクセサリ/ケース・カバー']

for a_category in a_categories:
    target = category[category['Amazonカテゴリ名'] == a_category]['ヤフオクカテゴリ名'].values[0]
    print(target)
