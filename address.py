from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# 파일을 읽어드려서 데이터 베이스에 저장
def address_to_database():
    f = open("./address.txt", 'r', encoding='UTF8')

    lines = f.readlines()
    for line in lines:
        if '폐지' not in line:
            address_arr = line.split()
            # address = {'info': line.split()}
            if len(address_arr) == 3:
                address = {
                    'code': address_arr[0].strip("0"),
                    'sido': address_arr[1],
                    'gugun': address_arr[2]
                }
                db.addresses.insert_one(address)
            else:
                address = {
                    'code': address_arr[0].strip("0"),
                    'sido': address_arr[1],
                    'gugun': address_arr[2],
                    'dong': address_arr[3]
                }
                db.addresses.insert_one(address)
    f.close()

# 저장된 주소데이터에서 시,도 정보를 출력
def list_do():
    addresses = list(db.addresses.find({"$or":[{'$where': "this.code.length <= 2"}, {'code':'3611'}]}))
    for address in addresses:
        print(address)

def test_0(code):
    print(code.strip("0"))


# 함수 실행
address_to_database()
# list_do()