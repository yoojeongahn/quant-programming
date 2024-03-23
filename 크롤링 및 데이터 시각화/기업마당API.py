import requests as rq
from bs4 import BeautifulSoup
url = 'https://www.bizinfo.go.kr/uss/rss/bizinfoApi.do?crtfcKey=QJ9ENB&dataType=json&hashtags=중소기업'
api_key = 'QJ9ENB'

res = rq.get(url).json()
cnt = 0
for i in res['jsonArray']:
    # print(i)
    cnt += 1

print(cnt)
