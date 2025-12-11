from motor.motor_asyncio import AsyncIOMotorClient
from .settings import settings

class MongoDB:
    """MongoDB connection manager."""
    
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB."""
        cls.client = AsyncIOMotorClient(settings.mongodb_uri)
        print(f"Connected to MongoDB at {settings.mongodb_uri}")
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            print("Closed MongoDB connection")
    
    @classmethod
    def get_database(cls):
        """Get the database instance."""
        return cls.client[settings.database_name]


def get_db():
    """Dependency to get database instance."""
    return MongoDB.get_database()
