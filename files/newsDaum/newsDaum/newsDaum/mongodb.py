import pymongo

client = pymongo.MongoClient("mongodb://")
db = client.daum
collection = db.article
