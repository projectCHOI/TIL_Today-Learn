import requests
import csv
from bs4 import BeautifulSoup

for date in range(20230831, 20230800, -1):

    print(date)
    file = open(f"{date}.csv", mode="w", encoding="utf-8", newline="")
    writer = csv.writer(file)

    page = 1

    while True:
        
        print(page)
        
        params = {
            'mode': 'LPOD',
            'oid': '001',
            'date': date,
            'page': page
        }

        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        response = requests.get('https://news.naver.com/main/list.naver', headers=headers, params=params)
        bs = BeautifulSoup(response.text, 'html.parser')

