#기사의 페이지 갯수
import requests
from bs4 import BeautifulSoup

URL = "https://search.naver.com/search.naver?where=news&query=%22%EB%AC%BB%EC%A7%80%EB%A7%88%25%EB%B2%94%EC%A3%84%22&sm=tab_opt&sort=0&photo=0&field=0&pd=5&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1y&is_sug_officeid=0&office_category=0&service_area=0"
#위 링크는 네이버 뉴스의 23.09.21 기준/지난 1년간 "묻지마 범죄"에 대한 기사 페이지이다.
res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")

news_list = soup.select("ul.list_news li")
#1news_list = soup.select("ul.list_news li")는 soup 객체를 사용하여 HTML에서 뉴스 목록을 선택합니다. 
#2이 선택자 "ul.list_news li"는 <ul> 태그 중에서 class 속성이 "list_news"인 것을 선택하고, 그 안에 있는 <li> 태그를 모두 선택합니다.
#3이렇게 선택한 뉴스 목록 항목들은 news_list라는 리스트에 저장됩니다.

len(news_list)
#news_list 리스트의 길이를 계산합니다. 이 값은 뉴스 목록에 있는 항목의 수를 나타냅니다.