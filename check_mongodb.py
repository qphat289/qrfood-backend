"""
MongoDB Connection Checker
This script checks if MongoDB is running and accessible
"""

import sys
from database import init_database, get_db

def check_mongodb():
    """Check MongoDB connection and basic functionality"""
    
    print("🔍 Checking MongoDB Connection")
    print("=" * 40)
    
    # Try to connect
    print("1. Testing database connection...")
    if not init_database():
        print("❌ Failed to connect to MongoDB")
        print("\n💡 Troubleshooting tips:")
        print("   - Make sure MongoDB is installed and running")
        print("   - Check if MongoDB service is started:")
        print("     Windows: net start MongoDB")
        print("     macOS: brew services start mongodb-community")
        print("     Linux: sudo systemctl start mongod")
        print("   - Verify the MONGO_URI in your configuration")
        return False
    
    print("✅ Successfully connected to MongoDB")
    
    # Test basic operations
    try:
        db = get_db()
        
        print("\n2. Testing database operations...")
        
        # Test ping
        db.command('ping')
        print("✅ Database ping successful")
        
        # Test collections access
        collections = db.list_collection_names()
        print(f"✅ Found {len(collections)} collections: {collections}")
        
        # Test document count
        users_count = db.users.count_documents({})
        posts_count = db.posts.count_documents({})
        print(f"✅ Database statistics:")
        print(f"   Users: {users_count}")
        print(f"   Posts: {posts_count}")
        
        if users_count == 0 and posts_count == 0:
            print("\n💡 Your database is empty. Run 'python seed_database.py' to add sample data.")
        
        print("\n🎉 MongoDB is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Database operation failed: {e}")
        return False

def show_next_steps():
    """Show what to do next"""
    print("\n📋 Next Steps:")
    print("1. If database is empty, run: python seed_database.py")
    print("2. Start the Flask server: python app.py")
    print("3. Test the API: python test_api.py")
    print("4. Visit http://localhost:5000 in your browser")

if __name__ == "__main__":
    print("🚀 MongoDB Connection Checker")
    print("This tool verifies your MongoDB setup\n")
    
    success = check_mongodb()
    
    if success:
        show_next_steps()
    else:
        print("\n❌ Please fix the MongoDB connection issues before proceeding.")
        sys.exit(1)
