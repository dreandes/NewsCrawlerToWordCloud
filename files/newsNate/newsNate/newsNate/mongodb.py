import pymongo

client = pymongo.MongoClient("mongodb://")
# db = client.nate
# collection = db.article
db_nate = client.nate
collection_nate = db_nate.article
db = client.all
collection_all = db.article
