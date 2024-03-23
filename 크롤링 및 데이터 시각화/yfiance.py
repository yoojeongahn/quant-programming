import yfinance as yf   # https://pypi.org/project/yfinance/
import matplotlib.pyplot as plt
import numpy as np

sp = yf.Ticker("HYG")
# get historical market data
hist = sp.history(start="1990-01-01", end=None)
# hist = sp.get_shares_full(start="1990-01-01", end=None)
print(hist['Close'])

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(np.log(hist['Close']), label='TMF', color='green')
ax1.axhline(y=0, color='r', linestyle='dashed')
ax1.set_ylabel('장단기 금리차')
ax1.legend(loc='lower right')

plt.show()