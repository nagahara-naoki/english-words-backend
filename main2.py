import requests
from bs4 import BeautifulSoup
from utils import save_to_file

res = requests.get('https://www.rarejob.com/englishlab/column/20210922_04/')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')


def main():
    data_list = []
    id_counter = 0
    fileName = ''
    ttale = soup.find_all('table')

    for tableInt, table in enumerate(ttale):
        id_counter = 1
        data_list = {}
        tbodys = table.find_all('tbody')  # 各テーブルの tbody を取得
        for tbody in tbodys:
            rows = tbody.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    word = cols[1].get_text(strip=True)
                    desc = cols[2].get_text(strip=True)
                    data_list[id_counter] = {
                        'word': word,
                        'desc': desc
                    }
                    id_counter += 1
                    fileName = 'toeic' + str(tableInt+1)
        save_to_file(data_list, fileName)
    return data_list


main()
