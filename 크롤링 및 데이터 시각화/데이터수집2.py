## 공시데이터 수집
import requests as rq
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

api_key = '08e5db49a5cb6f650e1f59ce55b19100ef0cc938'

bgn_date = (date.today() + relativedelta(days=-7)).strftime("%Y%m%d")
end_date = (date.today()).strftime("%Y%m%d")

notice_url = f'''https://opendart.fss.or.kr/api/list.json?crtfc_key={api_key}
&bgn_de={bgn_date}&end_de={end_date}&page_no=1&page_count=100'''

notice_data = rq.get(notice_url)
notice_data_df = notice_data.json().get('list')
notice_data_df = pd.DataFrame(notice_data_df)
# print(notice_data_df)


# 삼성전자 공시 데이터 수집
corp_code = '00126380'  # 삼성전자 고유번호
bgn_date = (date.today() + relativedelta(days=-30)).strftime("%Y%m%d")
end_date = (date.today()).strftime("%Y%m%d")

notice_url_ss = f'''https://opendart.fss.or.kr/api/list.json?crtfc_key={api_key}
&corp_code={corp_code}&bgn_de={bgn_date}&end_de={end_date}&page_no=1&page_count=100'''

notice_data_ss = rq.get(notice_url_ss)
notice_data_ss_df = notice_data_ss.json().get('list')
notice_data_ss_df = pd.DataFrame(notice_data_ss_df)

# print(notice_data_ss_df.tail())

notice_url_exam = notice_data_ss_df.loc[0, 'rcept_no']
notice_dart_url = f'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={notice_url_exam}'
# print(notice_dart_url)    공시번호 + url    ->  사업보고서


# 사업보고서 주요 정보
bsns_year = '2021'      # 사업연도(4자리)
reprt_code = '11011'    # 보고서 코드 | 1분기보고서 : 11013, 반기보고서 : 11012, 3분기보고서 : 11014, 사업보고서 : 11011

url_div = f'''https://opendart.fss.or.kr/api/alotMatter.json?crtfc_key={api_key}
&corp_code={corp_code}&bsns_year={bsns_year}&reprt_code={reprt_code}'''

div_data_ss = rq.get(url_div)
div_data_ss_df = div_data_ss.json().get('list')
div_data_ss_df = pd.DataFrame(div_data_ss_df)

print(div_data_ss_df.head())


