## 모멘텀 전략

import pandas_datareader.data as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

df_mom = web.DataReader('10_Portfolios_Prior_12_2',
                        'famafrench',
                        start='1900-01-01'
                        )
df_mom_vw = df_mom[0]
df_mom_cum = np.log(1 + df_mom_vw / 100).cumsum()

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

df_mom_cum.plot(figsize=(10, 6),
                colormap=cm.jet,
                legend='rev1erse',
                title='모멘텀별 포트폴리오의 누적 수익률')
# plt.show()

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

# print(factor_stat(df_mom_vw))     포트폴리오별 통계값을 확인

# 모멘텀 포트폴리오 구하기
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:ssafy@127.0.0.1:3306/stock_db')

ticker_list = pd.read_sql(
"""
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker) 
	and 종목구분 = '보통주';
""", con=engine)


price_list = pd.read_sql(
"""
select 날짜, 종가, 종목코드
from kor_price
where 날짜 >= (select (select max(날짜) from kor_price) - interval 1 year);
""", con=engine)    # 최근 1년치 가격 정보

engine.dispose()

price_pivot = price_list.pivot(index='날짜', columns='종목코드', values='종가')
price_pivot.iloc[0:5, 0:5]

ret_list = pd.DataFrame(data=(price_pivot.iloc[-1] / price_pivot.iloc[0]) - 1,
                        columns=['return'])
data_bind = ticker_list[['종목코드', '종목명']].merge(ret_list, how='left', on='종목코드')

print(data_bind.head())
