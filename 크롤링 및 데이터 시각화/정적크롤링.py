import requests as rq
from bs4 import BeautifulSoup
import time

url = 'https://quotes.toscrape.com/'
quote = rq.get(url)

quote_html = BeautifulSoup(quote.content, 'html.parser')    # BeautifulSoup(quote.content, 'xml')
quote_div = quote_html.find_all('div', class_='quote')      # find() -> class가 quote인 div태그 추출

quote_span = quote_div[0].find_all('span', class_='text')   # quote_span[0].text
#   print([i.find_all('span', class_ ='text')[0].text for i in quote_div])

quote_text = quote_html.select('div.quote > span.text')     # select() -> find_all() 함수 대체
quote_text_list = [i.text for i in quote_text]

quote_author = quote_html.select('div.quote > span > small.author')
quote_author_list = [i.text for i in quote_author]

quote_link = quote_html.select('div.quote > span > a')      # print(quote_link[0]['href'])
quote_link_list = ['https://quotes.toscrape.com' + i['href'] for i in quote_link]   # 완전한 URL 만들기