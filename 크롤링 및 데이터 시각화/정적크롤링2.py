import requests as rq
from bs4 import BeautifulSoup
import time
import pandas as pd
text_list = []
author_list = []
infor_list = []

for i in range(1, 100):
    url = f'https://quotes.toscrape.com/page/{i}/'
    quote = rq.get(url)
    quote_html = BeautifulSoup(quote.content, 'html.parser')

    quote_text = quote_html.select('div.quote > span.text')
    quote_text_list = [i.text for i in quote_text]

    quote_author = quote_html.select('div.quote > span > small.author')
    quote_author_list = [i.text for i in quote_author]

    quote_link = quote_html.select('div.quote > span > a')
    quote_link_list = ['https://quotes.toscrape.com' + i['href'] for i in quote_link]

    if len(quote_text_list) > 0:
        text_list.extend(quote_text_list)
        author_list.extend(quote_author_list)
        infor_list.extend(quote_link_list)
        time.sleep(1)
    else:
        break

print(pd.DataFrame({'text': text_list, 'author': author_list, 'infor': infor_list}))