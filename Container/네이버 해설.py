import requests
from bs4 import BeautifulSoup

#이건 url 페이지가 넘어가게 해준다.
#함수는 range을 사용한다. range(시작, 끝)의 양식
for page_url in range(2, 5):
    #page_url을 2-5까지의 숫자로 바꾼다는 뜻,
    #print(page_url) 이건 확인용이다.
    url = f'https://finance.naver.com/item/sise_day.naver?code=005930&page={page_url}'
    #url 앞에 [f]를 넣어야 뒤에 {page_url}가 숫자가 되어 카운트 된다.
    
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

            date = data.select('td')[0].text
            #찾아라. 데이터 td 값에서 0번째 텍스트를
            #추가. 여기서 td의 0번째 텍스트가 날짜임

            stock_price = data.select('td')[1].text
            #찾아라. 데이터 td 값에서 1번째 텍스트를
            #추가. 여기서 td의 1번째 텍스트가 가격임

            print(date, stock_price)
