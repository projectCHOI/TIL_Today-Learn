import requests
from bs4 import BeautifulSoup
import csv

file = open("230919_naver-J.csv", mode="w", encoding="utf-8", newline="")
writer = csv.writer(file)

for page_url in range(1, 5):
    url = f'https://finance.naver.com/item/sise_day.naver?code=005930&page={page_url}'
    
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

    response = requests.get(url, headers=headers)

    page_content = response.text
    soup = BeautifulSoup(page_content, 'html.parser')

    #찾기 시작
    for data in soup.select('table.type2 tr'):
    #찾아라. (soup)에서 (table.type2)를 그리고 내부에 tr을.
        if len(data.select('td')) >= 7:
        #만약. data에서 td 값이 7 이상일 때
            writer.writerow([data.select('td')[0].text.replace('.','-'),
                            data.select('td')[1].text.replace(',','')])
file.close()
#print(date, stock_price