## 밸류 포트폴리오 구하기

from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine('mysql+pymysql://root:ssafy@127.0.0.1:3306/stock_db')

ticker_list = pd.read_sql("""
select * from kor_ticker
    where 기준일 = (select max(기준일) from kor_ticker) 
        and 종목구분 = '보통주';
""", con=engine)

value_list = pd.read_sql("""
select * from kor_value
    where 기준일 = (select max(기준일) from kor_value);
""", con=engine)

engine.dispose()

value_list.loc[value_list['값'] <= 0, '값'] = np.nan
value_pivot = value_list.pivot(index='종목코드', columns='지표', values='값')  # pivot() 함수를 통해 가치지표 테이블을 가로로 긴 형태로 변경
data_bind = ticker_list[['종목코드', '종목명']].merge(value_pivot,
                                               how='left',
                                               on='종목코드')

# print(data_bind.head())

value_rank = data_bind[['PER', 'PBR']].rank(axis=0)     # rank() 함수를 통해 PER와 PBR 열의 순위를 열 방향(axis = 0)으로
value_sum = value_rank.sum(axis=1, skipna=False).rank() # 행 방향으로 값을 합산
# print(data_bind.loc[value_sum<=20, ['종목코드', '종목명', 'PER', 'PBR']])    # 순위가 낮은 20 종목


## 여러 지표 결합하기
import matplotlib.pyplot as plt
import seaborn as sns

value_list_copy = data_bind.copy()
value_list_copy['DY'] = 1 / value_list_copy['DY']   #  DY의 경우 값이 높을수록 배당수익률이 높은 가치주에 해당한다. 따라서 DY에 역수를 취해 순서를 맞춰준다.
value_list_copy = value_list_copy[['PER', 'PBR', 'PCR', 'PSR', "DY"]]
value_rank_all = value_list_copy.rank(axis=0)
mask = np.triu(value_rank_all.corr())

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(value_rank_all.corr(),
            annot=True,
            mask=mask,
            annot_kws={"size": 16},
            vmin=0,
            vmax=1,
            center=0.5,
            cmap='coolwarm',
            square=True)
ax.invert_yaxis()
plt.show()

value_sum_all = value_rank_all.sum(axis=1, skipna=False).rank()
print(data_bind.loc[value_sum_all <= 20])
