from selenium import webdriver  # pip install webdriver-manager update
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

# 브라우저 자동 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
url = 'https://www.naver.com/'
driver.get(url)

# driver.find_element(By.LINK_TEXT, value='뉴스').click()     뉴스 버튼 클릭
# driver.switch_to.window(driver.window_handles[0])           탭 focus 위치
# driver.find_element(By.CLASS_NAME, value='btn_search').send_keys(Keys.ENTER)
# driver.find_element(By.ID, value='query').clear()

driver.find_element(By.ID, value='query').send_keys('이현열 퀀트')
driver.find_element(By.CLASS_NAME, value='btn_search').click()

# 개발자 도구로 Xpath Copy
# driver.find_element(By.XPATH, value='//*[@id="main_pack"]/section[5]/div/div[1]/div[2]/a[2]').click()
# driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')    # 페이지 스크롤 이동

prev_height = driver.execute_script('return document.body.scrollHeight')
# driver.find_element(By.TAG_NAME, value = 'body').send_keys(Keys.PAGE_DOWN)

## 2초 슬립하면서 스크롤 최하단까지
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)

    curr_height = driver.execute_script('return document.body.scrollHeight')
    if curr_height == prev_height:
        break
    prev_height = curr_height

html = BeautifulSoup(driver.page_source, 'lxml')
txt = html.find_all(class_='title_link')
txt_list = [i.get_text() for i in txt]
print(txt_list[0:10])

# driver.quit()

'''
webdriver.Chrome(): 브라우저 열기
driver.close(): 현재 탭 닫기
driver.quit(): 브라우저 닫기
driver.back(): 뒤로 가기
driver.forward(): 앞으로 가기

By.ID: 태그의 ID 값으로 추출
By.NAME: 태그의 NAME 값으로 추출
By.XPATH: 태그의 XPATH 값으로 추출
By.LINK_TEXT: 링크에 존재하는 텍스트로 추출
By.TAG_NAME: 태그명으로 추출
By.CLASS_NAME: 태그의 클래스명으로 추출
By.CSS_SELECTOR: CSS 선택자로 추출

click(): 엘레먼트를 클릭
clear(): 텍스트 삭제
send_keys(text): 텍스트 입력
send_keys(Keys.CONTROL + 'v'): 컨트롤 + v 누르기
'''