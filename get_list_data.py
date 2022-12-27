from genericpath import isfile
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from settings import *

# ページID保存用ログファイルからIDを取得する
def read_log_file_id() :
    id = 1
    if os.path.isfile(LOG_FILE_ID) :
        with open(LOG_FILE_ID) as f:
            s = f.read().strip()
            if str.isdigit(s) :
                id = int(s)
    return id

# ページID保存用ログファイルに書き出す
def write_log_file_id(id) :
    with open(LOG_FILE_ID, "w") as f :
        f.write(str(id))

# ページIDの初期値を取得
id = read_log_file_id()

# 既に出力済みのcsvを読み込み
df_all = pd.DataFrame()
if os.path.isfile(CSV_FILE_LIST) :
    df_all = pd.read_csv(CSV_FILE_LIST, header=0, index_col=0)
print(df_all)

# ページ読み込みループ
for i in range(MAX_READ_PAGE_NUM_LIST) :
    # HTML取得
    url = BASE_URL.format(id)
    response = requests.get(url)
    if not response or response.status_code != requests.codes.ok or response.url != url :
        break
    soup = BeautifulSoup(response.text, 'html.parser')

    # リスト取得
    ul = soup.select("[class='list clearfix']")
    if len(ul) <= 0 :
        break

    # リストループ
    table = []
    for box in ul :
        # 要素取得
        title = box.select_one(".title")
        a = title.select_one("a")
        price = box.select_one(".price").select(".right")
        other = box.select_one(".other").select_one(".right")

        # テーブル作成
        line = []
        line.append(a.get("href"))
        line.append(a.text)
        if len(price) > 0 :
            line.append(price[0].text.replace(",", ""))
        else :
            line.append("")
        if len(price) > 1 :
            line.append(price[1].text.replace(",", ""))
        else :
            line.append("")
        line.append(other.text)
        table.append(line)

    # 取得結果をDataFrameに結合
    df = pd.DataFrame(table, columns=LIST_COL_NAME_LIST)
    print(df)
    df_all = pd.concat([df_all, df], ignore_index=True, sort=False)

    # ページIDインクリメント
    id = id + 1

# csv出力&ページIDログ出力
if len(df_all) > 0 :
    df_all.to_csv(CSV_FILE_LIST, header=True, index=True, mode="w")
    write_log_file_id(id)
