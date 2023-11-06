#찾는 키워드 칼부림
#기간 "2023.08.22"~ "2023.09.22"
#페이지 내부 뉴스기사 가져오기

import requests
import pandas as pd
from bs4 import BeautifulSoup

keyword = "칼부림"
startdate = "2023.08.22"
enddate = "2023.09.22"

def get_news_list(keyword, startdate, enddate) :
    
    URL = "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EC%B9%BC%EB%B6%80%EB%A6%BC&oquery=%EB%AC%BB%EC%A7%80%EB%A7%88+%EB%B2%94%EC%A3%84&tqi=id14Psp0YidssSphNpNssssssyN-385831&nso=so%3Ar%2Cp%3Afrom20230822to20230922%2Ca%3Aall&de=2023.09.22&ds=2023.08.22&mynews=0&office_category=0&office_section_code=0&office_type=0&pd=3&photo=0&service_area=0&sort=2"
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    news_list = soup.select("ul.list_news li")
    
    li = []
    for item in news_list :
        if len(item.select("div.info_group a")) == 2 :
            li.append(get_news(item.select("div.info_group a")[1]['href']))
    
    return pd.DataFrame(li, columns=['title','date','media','content','url'])

get_news_list('칼부림', '2023.08.22', '2023.09.22')