# 마법공식
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

engine = create_engine('mysql+pymysql://root:ssafy@127.0.0.1:3306/stock_db')

value_list = pd.read_sql("""
select * from kor_value
where 기준일 = (select max(기준일) from kor_value)
and 지표 = 'PBR';
""", con=engine)

fs_list = pd.read_sql("""
select * from kor_fs
where 계정 in ('매출총이익', '자산')
and 공시구분 = 'y';
""", con=engine)

engine.dispose()

# 밸류 지표
value_list.loc[value_list['값'] < 0, '값'] = np.nan
value_pivot = value_list.pivot(index='종목코드', columns='지표', values='값')

# 퀄리티 지표
fs_list = fs_list.sort_values(['종목코드', '계정', '기준일'])
fs_list = fs_list.groupby(['종목코드', '계정']).tail(1)
fs_list_pivot = fs_list.pivot(index='종목코드', columns='계정', values='값')
fs_list_pivot['GPA'] = fs_list_pivot['매출총이익'] / fs_list_pivot['자산']

# 데이터 합치기
bind_rank = value_pivot['PBR'].rank().to_frame().merge(
    fs_list_pivot['GPA'].rank(ascending=False), how='inner', on='종목코드')

# 상관관계 (PER-GPA)
# print(bind_rank.corr())

bind_data = value_list.merge(fs_list_pivot, how='left', on='종목코드')
bind_data = bind_data.dropna()
bind_data['PBR_quantile'] = pd.qcut(bind_data['값'], q=5, labels=range(1, 6))
bind_group = bind_data.groupby('PBR_quantile').mean('GPA')

fig, ax = plt.subplots(figsize=(10, 6))
plt.rc('font', family='Malgun Gothic')
plt.bar(x=np.arange(5), height=bind_group['GPA'])
plt.xlabel('PBR')
plt.ylabel('GPA')

# plt.show()

url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_BEME_OP_5x5_CSV.zip'
df_qv = pd.read_csv(url, skiprows=21, encoding='cp1252', index_col=0)
end_point = np.where(pd.isna(df_qv.iloc[:, 2]))[0][0]
df_qv = df_qv.iloc[0:end_point].apply(pd.to_numeric)

# print(df_qv.head())


# 마법공식 포트폴리오(이익 수익률(Earnings Yield) & 투하자본 수익률(Return on Capital))
ticker_list = pd.read_sql("""
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker) 
and 종목구분 = '보통주';
""", con=engine)

fs_list = pd.read_sql("""
select * from kor_fs
where 계정 in ('매출액', '당기순이익', '법인세비용', '이자비용', '현금및현금성자산',
'부채', '유동부채', '유동자산', '비유동자산', '감가상각비')
and 공시구분 = 'q';
""", con=engine)

engine.dispose()

fs_list = fs_list.sort_values(['종목코드', '계정', '기준일'])
fs_list['ttm'] = fs_list.groupby(['종목코드', '계정'], as_index=False)['값'].rolling(
    window=4, min_periods=4).sum()['값']
fs_list_clean = fs_list.copy()
fs_list_clean['ttm'] = np.where(
    fs_list_clean['계정'].isin(['부채', '유동부채', '유동자산', '비유동자산']),
    fs_list_clean['ttm'] / 4, fs_list_clean['ttm'])

fs_list_clean = fs_list_clean.groupby(['종목코드', '계정']).tail(1)
fs_list_pivot = fs_list_clean.pivot(index='종목코드', columns='계정', values='ttm')

data_bind = ticker_list[['종목코드', '종목명', '시가총액']].merge(fs_list_pivot,
                                                       how='left',
                                                       on='종목코드')
data_bind['시가총액'] = data_bind['시가총액'] / 100000000

# 분자(EBIT)
magic_ebit = data_bind['당기순이익'] + data_bind['법인세비용'] + data_bind['이자비용']

# 분모
magic_cap = data_bind['시가총액']
magic_debt = data_bind['부채']

## 분모: 여유자금
magic_excess_cash = data_bind['유동부채'] - data_bind['유동자산'] + data_bind[
    '현금및현금성자산']
magic_excess_cash[magic_excess_cash < 0] = 0
magic_excess_cash_final = data_bind['현금및현금성자산'] - magic_excess_cash

magic_ev = magic_cap + magic_debt - magic_excess_cash_final

# 이익수익률
magic_ey = magic_ebit / magic_ev

# 투하자본 수익률
magic_ic = (data_bind['유동자산'] - data_bind['유동부채']) + (data_bind['비유동자산'] -
                                                      data_bind['감가상각비'])
magic_roc = magic_ebit / magic_ic

# 열 입력하기
data_bind['이익 수익률'] = magic_ey
data_bind['투하자본 수익률'] = magic_roc

magic_rank = (magic_ey.rank(ascending=False, axis=0) +
              magic_roc.rank(ascending=False, axis=0)).rank(axis=0)
data_bind.loc[magic_rank <= 20, ['종목코드', '종목명', '이익 수익률', '투하자본 수익률']].round(4)

data_bind['투자구분'] = np.where(magic_rank <= 20, '마법공식', '기타')

plt.subplots(1, 1, figsize=(10, 6))
sns.scatterplot(data=data_bind,
                x='이익 수익률',
                y='투하자본 수익률',
                hue='투자구분',
                style='투자구분',
                s=200)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()