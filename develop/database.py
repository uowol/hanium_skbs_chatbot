import pymongo

# database 연결
def connect_database(db):
    connect_to = pymongo.MongoClient("mongodb+srv://uowon:sk1346@cluster0.zvgmaaw.mongodb.net/test")
    mdb = connect_to[db]
    return mdb

# collection 연결
def use(db, collection):
    return db[collection]

def insert(collection, data_list):
    collection.insert_many(data_list)

def find(collection, options = {}):
    searched = collection.find(options)
    return searched

def update(collection, options = {}):
    collection.update_many(options)

def delete(collection, options = {}):
    collection.delete_many(options)