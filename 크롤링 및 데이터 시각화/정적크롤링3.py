## 금융 속보 크롤링
import requests as rq
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258'
data = rq.get(url)
html = BeautifulSoup(data.content, 'html.parser')

# 실시간 속보의 제목 부분 HTML
html_select = html.select('dl > dd.articleSubject > a')
title_list = [i['title'] for i in html_select]
# print(title_list)


## 국가별 시가총액 데이터
import pandas as pd
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_stock_market_capitalization'
tbl = pd.read_html(url)
#print(tbl[0].head())


## 기업공시채널에서 오늘의 공시 불러오기
url = 'https://kind.krx.co.kr/disclosure/todaydisclosure.do?method=searchTodayDisclosureMain&marketType=0'
payload = {
    'method': 'searchTodayDisclosureSub',
    'currentPageSize': '15',
    'pageIndex': '1',
    'orderMode': '0',
    'orderStat': 'D',
    'forward': 'todaydisclosure_sub',
    'chose': 'S',
    'todayFlag': 'N',
    'selDate': '2022-07-27'
}

data = rq.post(url, data=payload)
html = BeautifulSoup(data.content, 'html.parser')
html_unicode = html.prettify()  # prettify() -> parser tree를 unicode로 변환
tbl = pd.read_html(html.prettify())
print(tbl[0].head())