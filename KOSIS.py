import requests
from urllib.request import urlopen
from urllib.parse import urlencode
import json
from datetime import datetime
import pandas as pd
import sqlite3

api_key = API_KEY
url = 'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList'

org_id = '101'
tbl_id = 'DT_1C8014'

prd_se = {
    'daily' : 'D',
    'monthly' : 'M',
    'quarterly' : 'Q',
    'semiannually' : 'H',
    'annually' : 'Y',
    'irreguarly' : 'IR',
}
period = 'monthly'

start_date = datetime(1990, 1, 1)
end_date = datetime(2022, 10, 15)
if period in ['daily', 'irreguarly']:
    startPrdDe = start_date.strftime('%Y%m%d')
    endPrdDe = end_date.strftime('%Y%m%d')
elif period in ['monthly', 'quarterly', 'semiannually']:
    startPrdDe = start_date.strftime('%Y%m')
    endPrdDe = end_date.strftime('%Y%m')
elif period == 'annually':
    startPrdDe = start_date.strftime('%Y')
    endPrdDe = end_date.strftime('%Y')
else:
    raise ValueError

item_id = 'T1'
obj_l1 = 'A01 B02 C03'

newest_counts = '20'
format = 'json'    

params = {
    # 'apiKey' : api_key,  
    'orgId' : org_id,
    'tblId' : tbl_id,
    'objL1' : obj_l1,
    # 'objL2' : '',
    # 'objL3' : '',
    # 'objL4' : '',
    # 'objL5' : '',
    # 'objL6' : '',
    # 'objL7' : '',
    # 'objL8' : '',
    'itmId' : item_id,
    'prdSe' : prd_se[period],
    'startPrdDe' : startPrdDe,
    'endPrdDe' : endPrdDe,
    'format' : format,
    'jsonVD' : 'Y',  
    # 'newEstPrdCnt' : newest_counts,
}

# url_KOSISgenerated = 'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=ZTk0ZWQ5OTAwYjg0YjhkYjhmZjBiOWNmZjlhNDM2Njg=&itmId=T1+&objL1=B02+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=199001&endPrdDe=202208&orgId=101&tblId=DT_1C8014'
url_combined = url + '&apiKey=' + api_key + '&' + urlencode(params)

print(urlencode(params))
print(url_combined)
with urlopen(url_combined) as data_received:
    data_read = data_received.read()
data_json = json.loads(data_read.decode('utf-8'))


print(data_json)

# df = pd.DataFrame([])
# for i in data_json:
#     # adding = pd.Series(i, name=i['PRD_DE'])   
#     adding = pd.Series({i['PRD_DE'] : i['DT']})
#     # print(adding) 
#     # df = pd.concat([df,adding], axis=1) #'axis=1' means the axis to concatenate along is columns
#     df = pd.concat([df, adding])

# # df.iloc[:,0] = df.index
# # df.drop(df.columns[[0]], axis=1, inplace=True)
# df.columns = ['Coincident_Index']
# print(df.iloc[:10,:])

# # connection = sqlite3.connect('D:/myProjects/myKiwoom/Coincident_Index.db')
# connection = sqlite3.connect('Coincident_Index.db')
# df.to_sql('Coincident_Index', connection, if_exists='replace')

