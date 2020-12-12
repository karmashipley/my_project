from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

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
    # addresses = list(db.addresses.find({"$and": [{'$where': "this.code.length == 4"}, {'code':'/^'+sido_receive+'/'}]}, {'_id': False}))
    addresses = list(db.addresses.find({"$and": [{'code':'/^11/'}]}, {'_id': False}))
    return jsonify({'result': 'success', 'addresses': addresses})
#
#
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

