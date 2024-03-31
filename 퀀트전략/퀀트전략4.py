# 퀄리티(기업의 우량성) 전략 - 수익성, 안정성, 재무구조, 성장성, 재무신뢰도, 배당, 투자

# 수익성별 포트폴리오의 수익률
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Portfolios_Formed_on_OP_CSV.zip'
df_op = pd.read_csv(url, skiprows=24, encoding='cp1252', index_col=0)
end_point = np.where(pd.isna(df_op.iloc[:, 2]))[0][0]
df_op_vw = df_op.iloc[0:end_point][[
    'Lo 20', 'Qnt 2', 'Qnt 3', 'Qnt 4', 'Hi 20'
]].apply(pd.to_numeric)
df_op_cum = np.log(1 + df_op_vw / 100).cumsum()

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

df_op_cum.plot(figsize=(10, 6),
               colormap=cm.jet,
               legend='reverse',
               title='수익성별 포트폴리오의 누적 수익률')
# plt.show()

# 우량성 포트폴리오 구하기
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:ssafy@127.0.0.1:3306/stock_db')

ticker_list = pd.read_sql("""
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker) 
and 종목구분 = '보통주';
""", con=engine)

fs_list = pd.read_sql("""
select * from kor_fs
where 계정 in ('당기순이익', '매출총이익', '영업활동으로인한현금흐름', '자산', '자본')
and 공시구분 = 'q';
""", con=engine)

engine.dispose()

fs_list = fs_list.sort_values(['종목코드', '계정', '기준일'])
fs_list['ttm'] = fs_list.groupby(['종목코드', '계정'], as_index=False)['값'].rolling(
    window=4, min_periods=4).sum()['값']
fs_list_clean = fs_list.copy()
fs_list_clean['ttm'] = np.where(fs_list_clean['계정'].isin(['자산', '자본']),
                                fs_list_clean['ttm'] / 4, fs_list_clean['ttm'])
fs_list_clean = fs_list_clean.groupby(['종목코드', '계정']).tail(1)

fs_list_pivot = fs_list_clean.pivot(index='종목코드', columns='계정', values='ttm')
fs_list_pivot['ROE'] = fs_list_pivot['당기순이익'] / fs_list_pivot['자본']
fs_list_pivot['GPA'] = fs_list_pivot['매출총이익'] / fs_list_pivot['자산']
fs_list_pivot['CFO'] = fs_list_pivot['영업활동으로인한현금흐름'] / fs_list_pivot['자산']

quality_list = ticker_list[['종목코드', '종목명']].merge(fs_list_pivot,
                                                  how='left',
                                                  on='종목코드')
# print(quality_list.round(4).head())

quality_list_copy = quality_list[['ROE', 'GPA', 'CFO']].copy()
quality_rank = quality_list_copy.rank(ascending=False, axis=0)

import seaborn as sns

mask = np.triu(quality_rank.corr())
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(quality_rank.corr(),
            annot=True,
            mask=mask,
            annot_kws={"size": 16},
            vmin=0,
            vmax=1,
            center=0.5,
            cmap='coolwarm',
            square=True)
ax.invert_yaxis()
# plt.show()

quality_sum = quality_rank.sum(axis=1, skipna=False).rank()
print(quality_list.loc[quality_sum <= 20,
                 ['종목코드', '종목명', 'ROE', 'GPA', 'CFO']].round(4))