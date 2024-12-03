import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

class MongoDB:
    client: AsyncIOMotorClient = None

    @classmethod
    def connectDB(cls):
        if not cls.client:
            uri = os.getenv('db_connection_str')
            cls.client = AsyncIOMotorClient(uri)
        return cls.client

    @classmethod
    async def ping(cls):
        try:
            await cls.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")


# Initialize the database connection
db_client = MongoDB.connectDB()
students_collection = db_client['students_db']['students']

# Test the connection
if __name__ == "__main__":
    import asyncio
    asyncio.run(MongoDB.ping())
