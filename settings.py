# get_list_data 設定

# スクレイピング対象URL({}の中にIDが入る)
BASE_URL = "https://www.hmv.co.jp/search/advanced_1/category_1%2C106/formattype_1/keyword_super+eurobeat/pagenum_{}/pagesize_1/target_MUSIC/?freeword_adv=super+eurobeat&wordkind_adv=ALL&category_adv=1"

# ページID保存用ログファイル
LOG_FILE_ID = "log_id.txt"

# リスト出力csvファイル
CSV_FILE_LIST = "list.csv"

# CSV列名リスト
LIST_COL_NAME_LIST = ["URL", "name", "price", "sale_price", "other"]

# 最大読み込みページ数
MAX_READ_PAGE_NUM_LIST = 2



# get_detail_data 設定

# URLカラム番号
COLUMN_NUM_URL = 0

# インデックス番号保存用ログファイル
LOG_FILE_INDEX = "log_index.txt"

# 詳細情報出力用csvファイル
CSV_FILE_DETAIL = "detail.csv"

# CSV列名リスト
LIST_COL_NAME_DETAIL = ["title", "genre", "catalog_no", "label", "country"]

# 最大読み込みページ数
MAX_READ_PAGE_NUM_DETAIL = 2


