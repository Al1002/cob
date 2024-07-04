from pymongo import MongoClient


CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.10"
client = MongoClient(CONNECTION_STRING)

def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # Create the database for our example (we will use the same database throughout the tutorial
    return client['cob_db']

def get_result_table():
    return get_database()['container_results']

def save_results(result):
    get_result_table().insert_one(result)

def get_result(uuid):
    result_entry = get_result_table().find_one({"uuid": uuid})
    if result_entry == None:
        return None
    return result_entry['result']

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
    # Get the database
    db = get_database()
    collection = db["user_files"]
    
    result = collection.insert_one({'file.txt': "This is a file"}, False, None, "This is a comment")
    print(result)
    print(get_result_table().find_one({"uuid": "794c6a2e-64be-47c1-af78-d6e9550ac5ee"}))