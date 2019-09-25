from pymongo import MongoClient

def get_queries():
    # FIXME need to point to the correct endpoint
    client = MongoClient('127.0.0.1')
    db = client['cc-datalake']
    return db['raw_links'].find({})
