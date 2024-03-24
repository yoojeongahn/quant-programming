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