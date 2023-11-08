# selenium(셀레니움)을 활용해 토큰과 로그인 정보 자동화를 자동화 한다.
# selenium은 웹 브라우저의 자동화 프로그램이다.
# 켜라, 움직여라, 가져와라 등등


# 순서1 : selenium(셀레니움)을 설치 
# 터미널에 설치
# pip install selenium==4.5
# pip install webdriver-manager

# 나는 설치는 파이썬 3.11.5에 깔려있다.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_experimental_option('detach', True) #브라우저 바로꺼짐 방지

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://n.news.naver.com/mnews/article/277/0005337370?sid=105')
driver.implicitly_wait(10)

#print(driver.find_element(By.CSS_SELECTOR, "h2#title_area").text)
time.sleep(5)

for li in driver.find_elements(By.CSS_SELECTOR, "li.u_likeit_list"):
    print(li)
#클릭

#검색어 임력

#