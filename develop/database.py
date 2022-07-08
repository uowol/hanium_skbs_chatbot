import pymongo

# mongo database 연결
def connect_database():
    connect_to = pymongo.MongoClient("localhost", 27017)
    mdb = connect_to.chat_db
    return mdb, mdb.chat

def insert(collection, data_list):
    collection.insert_many(data_list)

def find(collection, options = {}):
    searched = collection.find(options)
    return searched

def update(collection, options = {}):
    collection.update_many(options)

def delete(collection, options = {}):
    collection.delete_many(options)
