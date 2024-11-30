import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()

def connectDB():
    uri = os.getenv('db_connection_str')

    client = MongoClient(uri)

    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)


if __name__ == "__main__":
    connectDB()