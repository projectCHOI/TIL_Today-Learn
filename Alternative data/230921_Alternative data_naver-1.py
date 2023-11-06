import requests
from bs4 import BeautifulSoup

def get_news(URL) :
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # 기사 제목 가져오기
    title = soup.select_one("h2#title_area span").text.strip()
    # 기사 날짜 가져오기
    date = soup.select_one("span.media_end_head_info_datestamp_time")['data-date-time']
    #미디어 정보 가져오기 (선택자를 추가해야 함)
    media = soup.select_one("a.media_end_head_top_logo img")['title']
    #기사 내용 가져오기
    content = soup.select_one("article#dic_area").text.replace("\n","")
    
    #print를 return로 변경
    return (title, date, media, content, URL)

#출력변경
get_news("https://n.news.naver.com/mnews/article/052/0001938805?sid=105")