from pymongo import MongoClient

import uuid

CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.10"

class DBInterface:
    client = MongoClient(CONNECTION_STRING)
    database = client['cob_db']
    results = database['container_results']
    
    def save_result(self, result: str):
        self.results.insert_one(result)
    
    def result_exists(self, uuid: uuid.UUID) -> bool:
        result_entry = self.results.find_one({"uuid": uuid})
        return result_entry != None
        
    def get_result(self, uuid: uuid.UUID) -> None | dict:
        result_entry = self.results.find_one({"uuid": uuid})
        if result_entry == None:
            return None
        return result_entry

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
    # Get the database
    client = MongoClient(CONNECTION_STRING)
    db = client.get_database()
    collection = db["user_files"]
    result = collection.insert_one({'file.txt': "This is a file"}, False, None, "This is a comment")
    print(result)
    result = collection.find({})