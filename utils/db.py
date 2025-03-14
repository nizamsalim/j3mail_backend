from functools import wraps
from pymongo import MongoClient
from django.conf import settings

def singleton(cls):
    instances = {}
    @wraps(cls)
    def get_instance(*args,**kw_args):
        if cls not in instances:
            instances[cls] = cls(*args,**kw_args)
        return instances[cls]
    return get_instance

@singleton
class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.database = self.client[settings.MONGODB_NAME]
    def db(self,collection):
        return self.database[collection]
    def close(self):
        self.client.close()