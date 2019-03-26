import pandas as pd

# csvファイル名を入力
csv_file = input('CSVファイルの名前を入力してください: ') + '.csv'

df = pd.read_csv(csv_file)
counter = 0
print(df['商品名'].duplicated())
for i in df['商品名'].duplicated():
    if i:
        print(counter + 2)
        print(df['商品名'][counter])
    counter += 1