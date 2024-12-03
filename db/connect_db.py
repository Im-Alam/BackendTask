import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()


def connectDB():
    uri = os.getenv('db_connection_str')

    client = AsyncIOMotorClient(uri)

    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)

client = connectDB()
students_collection = client['students_db']['students']

if __name__ == "__main__":
    connectDB()