from genericpath import isfile
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from settings import *

# インデックス番号保存用ログファイルからIDを取得する
def read_log_file_index() :
    index = 0
    if os.path.isfile(LOG_FILE_INDEX) :
        with open(LOG_FILE_INDEX) as f:
            s = f.read().strip()
            if str.isdigit(s) :
                index = int(s)
    return index

# インデックス番号保存用ログファイルに書き出す
def write_log_file_index(index) :
    with open(LOG_FILE_INDEX, "w") as f :
        f.write(str(index))

# インデックス番号の初期値を取得
index = read_log_file_index()

# リスト出力csvファイル読み込み
df_list = pd.DataFrame()
if os.path.isfile(CSV_FILE_LIST) :
    df_list = pd.read_csv(CSV_FILE_LIST, header=0, index_col=0)
if len(df_list) <= index :
    exit

# 既に出力済みのcsvを読み込み
df_all = pd.DataFrame()
if os.path.isfile(CSV_FILE_DETAIL) :
    df_all = pd.read_csv(CSV_FILE_DETAIL, header=0, index_col=0)
print(df_all)

# リストループ
table = []
for i in range(MAX_READ_PAGE_NUM_DETAIL) :
    # URL取得
    row = index + i
    url = df_list.iat[row, COLUMN_NUM_URL]
    if not url or len(url) <= 0 :
        continue

    # HTML取得
    response = requests.get(url)
    if not response or response.status_code != requests.codes.ok or response.url != url :
        continue
    soup = BeautifulSoup(response.text, 'html.parser')

    # 情報取得、テーブル作成
    line = []
    block = soup.select_one("[class='singleMainBlock singleRelationsBlock clearfix js-floatingMenuAera']")
    main = block.select_one(".singleMainInfo")
    title = main.select_one(".title")
    if title and len(title) > 0 :
        line.append(title.text)
    else :
        line.append("")
    basic = block.select_one(".singleBasicInfo")
    info_list = basic.select(".right")
    if info_list and len(info_list) > 0 and info_list[0] and len(info_list[0]) > 0 :
        line.append(info_list[0].text.strip())
    else :
        line.append("")
    if info_list and len(info_list) > 1 and info_list[1] and len(info_list[1]) > 0 :
        line.append(info_list[1].text.strip())
    else :
        line.append("")
    if info_list and len(info_list) > 3 and info_list[3] and len(info_list[3]) > 0 :
        line.append(info_list[3].text.strip())
    else :
        line.append("")
    if info_list and len(info_list) > 4 and info_list[4] and len(info_list[4]) > 0 :
        line.append(info_list[4].text.strip())
    table.append(line)

# 取得結果をDataFrameに結合
df = pd.DataFrame(table, columns=LIST_COL_NAME_DETAIL)
print(df)
df_all = pd.concat([df_all, df], ignore_index=True, sort=False)

# csv出力&インデックス番号ログ出力
if len(df_all) > 0 :
    df_all.to_csv(CSV_FILE_DETAIL, header=True, index=True, mode="w")
    write_log_file_index(row + 1)
