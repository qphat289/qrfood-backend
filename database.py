import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

class DatabaseConfig:
    """MongoDB database configuration and connection"""
    
    def __init__(self):
        # MongoDB connection settings
        self.MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
        self.DATABASE_NAME = os.environ.get('DATABASE_NAME', 'qrfood_db')
        self.client = None
        self.db = None
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            # Create MongoDB client
            self.client = MongoClient(self.MONGO_URI)
            
            # Test the connection
            self.client.admin.command('ping')
            
            # Get database
            self.db = self.client[self.DATABASE_NAME]
            
            print(f"✅ Successfully connected to MongoDB: {self.DATABASE_NAME}")
            return True
            
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {e}")
            return False
    
    def get_database(self):
        """Get the database instance"""
        if self.db is None:
            self.connect()
        return self.db
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

# Global database instance
db_config = DatabaseConfig()

def get_db():
    """Get database instance"""
    return db_config.get_database()

def init_database():
    """Initialize database connection"""
    success = db_config.connect()
    if success:
        # Create indexes for better performance
        db = get_db()
        
        # Create index on email for users collection (unique)
        try:
            db.users.create_index("email", unique=True)
            print("✅ Created unique index on users.email")
        except Exception as e:
            print(f"Index creation info: {e}")
        
        # Create index on author_id for posts collection
        try:
            db.posts.create_index("author_id")
            print("✅ Created index on posts.author_id")
        except Exception as e:
            print(f"Index creation info: {e}")
            
    return success
