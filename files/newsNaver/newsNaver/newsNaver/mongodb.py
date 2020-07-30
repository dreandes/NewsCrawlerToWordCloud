import pymongo

client = pymongo.MongoClient("")
db = client.naver
collection = db.article
