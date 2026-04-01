import pymongo as pm
import json

class MongoInstance:

    def __init__(self, endpoint, auth = None, dbname = "database"):
        print("Initiating MongoInstance")
        self.endpoint = endpoint
        if auth == None:
            self.client = pm.MongoClient(f"mongodb://{endpoint}/")
        else:
            self.client = pm.MongoClient(f"mongodb://{auth}@{endpoint}/")
        self.db = self.client[dbname]
        if self.health():
            print(f"Serving on {endpoint}")
        else:
            print("Server error")

    def health(self):
        try:
            self.db.command('ping')
            return True
        except Exception as e:
            return False

    def create_collection(self, collection_name):
        try:
            #Check if exists
            for collec in self.db.list_collections():
                if collec["name"] == collection_name:
                    return {"error" : f"collection {collection_name} already exists"}

            collection = self.db.create_collection(name=collection_name, check_exists=False)
            return {"success" : f"collection {collection_name} created"}
        except Exception as e:
            return {"error" : f"error in creating collection {collection_name}", "message" : e}

    def find(self, collection, selection, projection = {}, one = False):
        try:
            if one:
                result = self.db[collection].find_one(selection, projection=projection)
            else:
                result = self.db[collection].find(selection, projection=projection)
            return result
        except Exception as e:
            return {"error" : "request error", "message" : e}

    def insert(self, collection, documents):
        try:
            if isinstance(documents, list):
                self.db[collection].insert_many(documents)
            else:
                self.db[collection].insert_one(documents)
            return {"success" : True}
        except Exception as e:
            return {"success" : False}

    def delete(self, collection, filter, one = False):
        try:
            if one:
                result = self.db[collection].delete_one(filter)
            else:
                result = self.db[collection].delete_many(filter)
            return {"success" : True, "deleted" : result.deleted_count}
        except Exception as e:
            return {"error" : "delete error", "message" : e}

    def count(self, collection, filter = {}):
        try:
            return self.db[collection].count_documents(filter)
        except:
            return -1

    def getCollection(self, collection_name):
        return self.db[collection_name]