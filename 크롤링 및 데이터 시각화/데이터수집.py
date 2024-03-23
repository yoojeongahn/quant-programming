## Dart 데이터 수집
import requests as rq
from io import BytesIO
import zipfile, json, pandas as pd, xmltodict
from sqlalchemy import create_engine

api_key = '08e5db49a5cb6f650e1f59ce55b19100ef0cc938'
codezip_url = f'''https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={api_key}'''
codezip_data = rq.get(codezip_url)
codezip_file = zipfile.ZipFile(BytesIO(codezip_data.content))
# print(codezip_file.namelist())    ->  ['CORPCODE.xml']

code_data = codezip_file.read('CORPCODE.xml').decode('utf-8')
data_odict = xmltodict.parse(code_data)
data_dict = json.loads(json.dumps(data_odict))
data = data_dict.get('result').get('list')
corp_list = pd.DataFrame(data)
# print(corp_list.head())

# 거래소에 등록되지 않은 코드 데이터 삭제
corp_list = corp_list[~corp_list.stock_code.isin(
    [None])].reset_index(drop=True)

# 로컬 root 계정으로 stock_db 스키마 내 dart_code 테이블 및 데이터 Insert
engine = create_engine('mysql+pymysql://root:ssafy@127.0.0.1:3306/stock_db')
# print(corp_list.to_sql(name='dart_code', con=engine, index=True, if_exists='replace'))

# print(corp_list[corp_list['corp_name'] == '삼성전자'])    -> '00126380'
