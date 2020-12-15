from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import pandas as pd

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## 광역시도 리스트 가져오기
@app.route('/do', methods=['GET'])
def list_do():
    addresses = list(db.addresses.find({"$or": [{'$where': "this.code.length <= 2"}, {'code': '3611'}]}, {'_id': False}))
    # print(addresses)
    return jsonify({'result': 'success', 'addresses': addresses})

## 시군구 리스트 가져오기
@app.route('/gugun', methods=['GET'])
def list_gugun():
    sido_receive = request.args.get('sido_give')
    addresses = list(db.addresses.find({"$and": [{'$where': "this.code.length == 4"}, {'code': {"$regex": '^'+sido_receive}}]}, {'_id': False}))
    for address in addresses:
        print(address)
    return jsonify({'result': 'success', 'addresses': addresses})

## 읍면동 리스트 가져오기
@app.route('/dong', methods=['GET'])
def list_dong():
    gugun_receive = request.args.get('gugun_give')
    addresses = list(db.addresses.find({"$and": [{'$where': "this.code.length == 8"}, {'code': {"$regex": '^'+gugun_receive}}]}, {'_id': False}))
    for address in addresses:
        print(address)
    return jsonify({'result': 'success', 'addresses': addresses})

## 실거래가 가져오기
@app.route('/price', methods=['GET'])
def get_items():
    url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?serviceKey=97cuqDDHG2c0S%2Bia01naWZSkqK5hz8svWszWFQ7h8pdi%2BUgafcVl4O9six0eKcmLe7BF%2FXMaOkrC4h%2Fc5dcofQ%3D%3D&pageNo=1&numOfRows=10&LAWD_CD=11110&DEAL_YMD=201512'
    params = {'serviceKey':'CpiOdC5ys8I193uQraXgAjdPTK0cjePBKcxRATkQIFNdg%2BiFRetQcI0fSNyWFM7klpIw%2Bk9zSaB%2BuotTe9%2FZPQ%3D%3D','pageNo':1,'numOfRows':10,'LAWD_CD':'11110','DEAL_YMD':'202010'}
    res = requests.get(url, params=params)
    root = ET.fromstring(res.content)
    item_list = []
    for child in root.find('body').find('items'):
        elements = child.findall("*")
        data = {}
        for element in elements:
            tag = element.tag.strip()
            text = element.text.strip()
            data[tag] = text
        item_list.append(data)
    return jsonify({'result': 'success', 'list': item_list})

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

# df = pd.DataFrame(item_list)
# items.head()

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

