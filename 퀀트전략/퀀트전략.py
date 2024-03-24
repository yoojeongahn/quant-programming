'''
팩터(Factor) - 주식의 수익률에 영향을 미치는 특성들
    조건 - 지속성, 범용성, 이해가능성, 강건성, 투자가능성

베타(Beta) - 주식시장의 변동에 반응하는 정도
    베타가 1이라는 뜻은 주식시장과 움직임이 정확히 같다는 뜻.
    주식시장에서 베타는 통계학의 회귀분석모형에서 기울기를 나타내는 베타와 의미가 같다.( y = a + bx)
    주식에 적용한 모형이 자산가격결정모형(CAPM: Capital Asset Pricing Model) (기대수익률 = 무위험수익률 + 위험프리미엄 * 베타(민감도))
'''

## 베타 계산하기
import warnings
warnings.filterwarnings(action='ignore')
import statsmodels.api as sm

import yfinance as yf
import pandas as pd

tickers = ['^KS11', '039490.KS']

all_data = {}
for ticker in tickers:
    all_data[ticker] = yf.download(ticker,
                                   start='2016-01-01',
                                   end='2021-12-31')
prices = pd.DataFrame({tic: data['Close'] for tic, data in all_data.items()})
ret = prices.pct_change().dropna()

# 알파(alpha) 값 계산하기
ret['intercept'] = 1    # 절편값 1 가정

# OLS() 함수  ->  선형회귀분석 실시   ->  회귀분석의 결과를 reg 변수에 저장.
reg = sm.OLS(ret[['039490.KS']], ret[['^KS11', 'intercept']]).fit()  # 증권주, 독립변수에는 KOSPI 지수 수익률 및 절편 입력
# print(reg.summary())
#   ^KS11 t value가 29(>2)이므로 유의하다고 볼 수 있다.
#   알파(intercept) t value 0.376으로 매우 낮아, 증권주의 수익률은 주식 시장에 대한 노출도인 베타를 제외하고 나면 초과 수익이 없다고 볼 수 있다.
# print(reg.params)   # 베타에 해당하는 값 확인

## 밸류 전략 - 낮은 가격의 주식(저PER, 저PBR 등)
import pandas_datareader as web
from pandas_datareader.famafrench import get_available_datasets

datasets = get_available_datasets()

# PBR별 포트폴리오의 수익률
df_pbr = web.DataReader('Portfolios_Formed_on_BE-ME',
                        'famafrench',
                        start='1900-01-01')

import matplotlib.pyplot as plt
from matplotlib import cm

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

df_pbr_vw = df_pbr[0].loc[:, ['Lo 20', 'Qnt 2', 'Qnt 3', 'Qnt 4', 'Hi 20']]
df_pbr_cum = (1 + df_pbr_vw/100).cumprod()  # 누적수익률
df_pbr_cum.plot(figsize=(10, 6),
                colormap=cm.jet,
                legend='reverse',
                title='PBR별 포트폴리오의 누적 수익률')
# plt.show()

import numpy as np
df_pbr_cum = np.log(1+df_pbr_vw/100).cumsum()
df_pbr_cum.plot(figsize=(10, 6),
                colormap=cm.jet,
                legend='reverse',
                title='PER별 포트폴리오의 누적 수익률')
# plt.show()

# 연율화 수익률(기하), 연율화 수익률(산술), 연율화 변동성 및 샤프지수를 구하는 함수를 만들기
def factor_stat(df):

    n = len(df)

    ret_ari = (df/100).mean(axis=0) * 12    # 산술평규
    ret_geo = (1 + df / 100).prod()**(12 / n) - 1   # 기하평균
    vol = (df / 100).std(axis=0) * np.sqrt(12)  # 변동성
    sharp = ret_ari / vol

    stat = pd.DataFrame(
        [ret_ari, ret_geo, vol, sharp],
        index=['연율화 수익률(산술)', '연율화 수익률(기하)', '연율화 변동성', '샤프지수']).round(4)

    stat.iloc[0:3, ] = stat.iloc[0:3, ] * 100

    return stat

print(factor_stat(df_pbr_vw))

# E/P(PER)
df_per = web.DataReader('Portfolios_Formed_on_E-P',
                        'famafrench',
                        start='1900-01-01')
df_per_vw = df_per[0].loc[:, ['Lo 20', 'Qnt 2', 'Qnt 3', 'Qnt 4', 'Hi 20']]
df_per_cum = np.log(1 + df_per_vw / 100).cumsum()
df_per_cum.plot(figsize=(10, 6),
                colormap=cm.jet,
                legend='reverse',
                title='PER별 포트폴리오의 누적 수익률')
# plt.show()

# CF/P(PCR)
df_pcr = web.DataReader('Portfolios_Formed_on_CF-P',
                        'famafrench',
                        start='1900-01-01')
df_pcr_vw = df_pcr[0].loc[:, ['Lo 20', 'Qnt 2', 'Qnt 3', 'Qnt 4', 'Hi 20']]
df_pcr_cum = np.log(1 + df_pcr_vw / 100).cumsum()
df_pcr_cum.plot(figsize=(10, 6),
                colormap=cm.jet,
                legend='reverse',
                title='PCR별 포트폴리오의 누적 수익률')
plt.show()