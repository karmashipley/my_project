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
    addresses = list(db.addresses.find({"$and": [{'$where': "this.code.length == 10"}, {'code': {"$regex": '^'+gugun_receive}}]}, {'_id': False}))
    for address in addresses:
        print(address)
    return jsonify({'result': 'success', 'addresses': addresses})

## 실거래가 가져오기
@app.route('/price', methods=['GET'])
def get_items():
    dongCode_receive = request.args.get('dongCode_give')
    yymm_receive = request.args.get('yymm_give')
    from_receive = request.args.get('from_give')
    to_receive = request.args.get('to_give')

    url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?LAWD_CD='+dongCode_receive[0:5]+'&DEAL_YMD='+yymm_receive+'&serviceKey=CpiOdC5ys8I193uQraXgAjdPTK0cjePBKcxRATkQIFNdg%2BiFRetQcI0fSNyWFM7klpIw%2Bk9zSaB%2BuotTe9%2FZPQ%3D%3D'
    res = requests.get(url)
    root = ET.fromstring(res.content)
    item_list = []
    for child in root.find('body').find('items'):
        elements = child.findall("*")

        check = False
        t_date = ''
        price = ''
        apt_name = ''
        for element in elements:
            tag = element.tag.strip()
            text = element.text.strip()
            if tag == '일':
                t_date = text
            if tag == '거래금액':
                price = text
            if tag == '아파트':
                apt_name = text
            if tag == '전용면적':
                square = text
            if tag == '층':
                floor = text
            dong_name = db.addresses.find_one({'code':dongCode_receive})['dong']
            if tag == '법정동' and text == dong_name:
                check = True
        if check:
            data = {'t_date': t_date, 'price': price, 'apt_name': apt_name, 'square': square, 'floor': floor}
            item_list.append(data)
    print(item_list)
    return jsonify({'result': 'success', 'list': item_list})


# df = pd.DataFrame(item_list)
# items.head()

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

