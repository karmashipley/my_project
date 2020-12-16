import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
# http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?serviceKey=97cuqDDHG2c0S%2Bia01naWZSkqK5hz8svWszWFQ7h8pdi%2BUgafcVl4O9six0eKcmLe7BF%2FXMaOkrC4h%2Fc5dcofQ%3D%3D&pageNo=1&numOfRows=10&LAWD_CD=11110&DEAL_YMD=201512
url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?serviceKey=97cuqDDHG2c0S%2Bia01naWZSkqK5hz8svWszWFQ7h8pdi%2BUgafcVl4O9six0eKcmLe7BF%2FXMaOkrC4h%2Fc5dcofQ%3D%3D&pageNo=1&numOfRows=10&LAWD_CD=11110&DEAL_YMD=201512'
params = {'serviceKey':'CpiOdC5ys8I193uQraXgAjdPTK0cjePBKcxRATkQIFNdg%2BiFRetQcI0fSNyWFM7klpIw%2Bk9zSaB%2BuotTe9%2FZPQ%3D%3D','pageNo':1,'numOfRows':10,'LAWD_CD':'11110','DEAL_YMD':'202010'}
res = requests.get(url, params=params)
tree = ET.fromstring(res.content)
items = tree.findall('body/items/item')
for item in items:
    print(item.find('법정동').text)
    print(item.find('거래금액').text)
    print(item.find('법정동읍면동코드').text)
    print(item.find('아파트').text)
    print(item.find('월').text)
