## FRED 데이터 다운로드
import pandas_datareader as web
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 10년 - 2년 장단기 금리차
t10y2y = web.DataReader('T10Y2Y', 'fred', start='1990-01-01')
# 10년 - 3개월 금리차
t10y3m = web.DataReader('T10Y3M', 'fred', start='1990-01-01')

rate_diff = pd.concat([t10y2y, t10y3m], axis=1)
rate_diff.columns = ['10Y - 2Y', '10Y -3M']
# print(rate_diff.tail())

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(t10y2y, color='black', linewidth=0.5, label='10Y-2Y')
ax1.plot(t10y3m, color='gray', linewidth=0.5, label='10Y-3M')
ax1.axhline(y=0, color='r', linestyle='dashed')
ax1.set_ylabel('장단기 금리차')
ax1.legend(loc='lower right')

# S&P500 주가지수 다운로드
import yfinance as yf

sp = yf.Ticker("^GSPC")
hist = sp.history(start="1990-01-01", end=None)
ax2 = ax1.twinx()
ax2.plot(np.log(hist['Close']), label='S&P500')
ax2.set_ylabel('S&P500 지수(로그)')
ax2.legend(loc='upper right')
# plt.show()


# TMF 주가지수 다운로드
tmf = yf.Ticker("TMF")
hist2 = tmf.history(start="1990-01-01", end=None)
ax3 = ax2.twinx()
ax3.plot(np.log(hist2['Close']), label='TMF', color='skyblue')
ax3.set_ylabel('TMF 지수(로그)')
ax3.legend(loc='upper left')
# plt.show()

# 기대 인플레이션 BEI 지수 = (5년물, 10년물) 국채 명목 금리 - (5년물, 10년물) TIPS 금리
bei = web.DataReader('T10YIE', 'fred', start='1990-01-01')  # 기대 인플레이션에 해당하는 코드
# print(bei.tail())

bei.plot(figsize=(10, 6), grid=True)
plt.axhline(y=2, color='r', linestyle='-')
# plt.show()


# Fear & Greed Index(공포와 탐욕 지수)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
url = 'https://edition.cnn.com/markets/fear-and-greed'
driver.get(url)
idx = driver.find_element(By.CLASS_NAME, value='market-fng-gauge__dial-number-value').text

driver.close()
idx = int(idx)

print(idx)