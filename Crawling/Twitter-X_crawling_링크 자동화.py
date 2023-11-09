#트윗터 자동 로그인

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_experimental_option('detach', True) #브라우저 바로꺼짐 방지

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#url은 트윗터 로그인 화면
driver.get('https://twitter.com/i/flow/login')
driver.implicitly_wait(10)

driver.find_element(By.CSS_SELECTOR, "input.r-30o5oe").send_keys('yoonsuk.choi@gmail.com')
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3")[8].click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "input.r-30o5oe").send_keys("01063108802")
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, "span.css-901oao")[6].click()
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, "input.r-30o5oe")[1].send_keys("abcd!@#$5678")
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3")[13].click()
time.sleep(1)

cookie_text = ''
csrf = ''

for cookie in driver.