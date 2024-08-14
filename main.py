from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from utils import save_to_file
import json
import random
from starlette.middleware.cors import CORSMiddleware  # 追加


url_list = [
    'https://agreatdream.com/word-list-senior-high-school-1st-year/',
    'https://agreatdream.com/word-list-senior-high-school-2nd-year/',
    'https://agreatdream.com/word-list-senior-high-school-3rd-year/'
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)


@app.get("/word-quiz/{category}/{quizCount}")
def read_item(category: str, quizCount: int):
    return get_json(category, quizCount)


def get_json(file_name, cout):
    full_path = f'JSON/{file_name}.json'
    with open(full_path, 'r', encoding='utf-8') as file:
        json_str = file.read()

    # 文字列をJSONオブジェクトに変換する
    data = json.loads(json_str)

    # 辞書のキーと値をリストとして取り出す
    items_list = list(data.items())

    # ランダムに10個のアイテムを選ぶ
    random_items = dict(random.sample(items_list, min(cout, len(items_list))))

    return random_items


def scrape_data(url):
    try:
        res = requests.get(url)
        res.encoding = 'utf-8'  # 明示的にエンコーディングを設定

        if res.status_code != 200:
            return []

        soup = BeautifulSoup(res.text, 'html.parser')
        title_text = soup.find_all('tbody')

        if not title_text:
            return []

        data_list = {}
        id_counter = 1

        for tbody in title_text:
            rows = tbody.find_all('tr')
            for row in rows:
                cols = [td for td in row.find_all(
                    'td') if td.get('bgcolor') != '#ffccff']
                if len(cols) >= 2:
                    word = cols[0].get_text(strip=True)
                    desc = cols[1].get_text(strip=True)
                    data_list[id_counter] = {
                        "word": word,
                        "desc": desc
                    }
                    id_counter += 1
        return data_list

    # エラーが発生した場合の処理
    except Exception as e:
        return []


def main():
    for i, url in enumerate(url_list):
        data = scrape_data(url)
        if data:
            filename = f'highschool{i + 1}.json'
            save_to_file(data, filename)


# if __name__ == '__main__':
#     main()
