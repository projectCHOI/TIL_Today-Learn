# csv 추가, time 추가, DataFrame 입력 방식 고정
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

def get_news(URL):
    try:
        res = requests.get(URL)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        title_element = soup.select_one('h2#title_area > span')
        content_element = soup.select_one('article#dic_area')
        date_element = soup.select_one('span._ARTICLE_DATE_TIME')

        if title_element and content_element and date_element:
            title = title_element.text  # 기사제목
            content = content_element.text.strip()  # 기사 내용
            date = date_element['data-date-time']  # 기사 날짜
            return (title, date, content)
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_news_list(keyword, startdate, enddate):
    data = []

    headers = {
        'Cookie': 'NNB=CJFYIM6TQT2WI; nx_ssl=2; page_uid=igWGllqo15Vssf9tLnVssssstcd-133196',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Referer': 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%97%90%EC%8A%A4%EC%9B%90&sort=0&photo=0&field=0&pd=3&ds=2023.10.25&de=2023.10.27&cluster_rank=19&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231025to20231027,a:all&start=11'
    }

    for nowdate in pd.date_range(startdate, enddate):
        nowdate = str(nowdate).replace('-', '.')[:10]
        page = 1

        while True:
            start = (page - 1) * 100 + 1
            URL = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&sort=1&photo=0&field=0&pd=3&ds={nowdate}&de={nowdate}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from{nowdate.replace(".","")},to{nowdate.replace(".","")},a:all&start={start}'
            try:
                res = requests.get(URL, headers=headers)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, 'html.parser')
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                break

            if not soup.select('ul.list_news'):
                break

            for li in soup.select('ul.list_news > li'):
                if len(li.select('div.info_group > a')) == 2:
                    news_data = get_news(li.select('div.info_group > a')[1]['href'])
                    if news_data:
                        data.append(news_data)

                page += 1

    df = pd.DataFrame(data, columns=['title', 'date', 'content']) #추가
    time.sleep(10)


    df.to_csv('21.csv', index=False, encoding='utf-8') # 이동

get_news_list('에스원', '2023.10.30', '2023.10.31')
