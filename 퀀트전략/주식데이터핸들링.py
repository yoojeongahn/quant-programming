import pickle
with open('C:/Users/YJA/Downloads/stock_db.pkl', 'rb') as f:
    data = pickle.load(f)

ticker_list = data[0]   # 티커
sector_list = data[1]   # 섹터
price_list = data[2]    # 주가
fs_list = data[3]       # 재무제표
value_list = data[4]    # 밸류지표(TTM)

print(fs_list)