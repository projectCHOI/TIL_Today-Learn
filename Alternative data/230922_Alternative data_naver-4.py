#문제 4번 : 페이지를 넘기자.
import requests
import pandas as pd
from bs4 import BeautifulSoup

#키워드 변수 추가
keyword = "칼부림"
startdate="2023.08.01"
enddate="2023.08.31"

#함수 get_news_list를 정의 
def get_news_list(keyword, startdate, enddate) :
  #il = [] 프레임에 출력 정보를 넣는다.
  li = []
  #h에 url 정보를 담는다.
  h = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

  #for 변수의 추가, start 1부터 100페이지까지
  for start in range(1,100) :

    URL = "https://search.naver.com/search.naver?where=news&query=%EC%B9%BC%EB%B6%80%EB%A6%BC&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds=2023.08.01&de=2023.08.31&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20230801to20230831&is_sug_officeid=0&office_category=0&service_area=0".format(keyword, startdate, enddate, startdate.replace(".",""), enddate.replace(".",""), start)

    res = requests.get(URL,headers = h)
    soup = BeautifulSoup(res.text, "html.parser")
    news_list = soup.select("ul.list_news li")
    
    for item in news_list :
      if len(item.select("div.info_group a")) == 2 :
        li.append(get_news(item.select("div.info_group a")[1]['href']))

  return pd.DataFrame(li, columns=['title','date','media','content','url'])

get_news_list('칼부림','2023.08.01', '2023.08.31')

#출력하면 693개의 데이터 출력
