"""
Database seeding script for QR Food Backend
This script populates the database with initial sample data
"""

from database import get_db, init_database
from datetime import datetime
from bson import ObjectId

def seed_database():
    """Seed the database with initial data"""
    
    print("🌱 Seeding database with initial data...")
    
    # Initialize database connection
    if not init_database():
        print("❌ Failed to connect to database")
        return False
    
    db = get_db()
    
    try:
        # Clear existing data (optional - remove if you want to keep existing data)
        print("🧹 Clearing existing data...")
        db.users.delete_many({})
        db.posts.delete_many({})
        
        # Sample users
        users_data = [
            {
                "name": "John Doe",
                "email": "john@example.com",
                "created_at": "2025-01-01T00:00:00Z"
            },
            {
                "name": "Jane Smith", 
                "email": "jane@example.com",
                "created_at": "2025-01-02T00:00:00Z"
            },
            {
                "name": "Alice Johnson",
                "email": "alice@example.com", 
                "created_at": "2025-01-03T00:00:00Z"
            }
        ]
        
        # Insert users
        print("👥 Creating sample users...")
        users_result = db.users.insert_many(users_data)
        user_ids = users_result.inserted_ids
        print(f"✅ Created {len(user_ids)} users")
        
        # Sample posts
        posts_data = [
            {
                "title": "Welcome to QR Food",
                "content": "This is our first post about the QR Food platform. We're excited to share this journey with you!",
                "author_id": str(user_ids[0]),
                "created_at": "2025-01-01T12:00:00Z"
            },
            {
                "title": "How to Use QR Codes for Food Ordering",
                "content": "QR codes make food ordering quick and contactless. Simply scan the code at your table and browse the menu!",
                "author_id": str(user_ids[1]),
                "created_at": "2025-01-02T14:30:00Z"
            },
            {
                "title": "Menu Management Tips",
                "content": "Keep your digital menu updated with seasonal items and pricing. Customer satisfaction depends on accurate information.",
                "author_id": str(user_ids[0]),
                "created_at": "2025-01-03T10:15:00Z"
            },
            {
                "title": "Customer Feedback Integration",
                "content": "We've added new features for collecting and managing customer feedback through our platform.",
                "author_id": str(user_ids[2]),
                "created_at": "2025-01-04T16:45:00Z"
            }
        ]
        
        # Insert posts
        print("📝 Creating sample posts...")
        posts_result = db.posts.insert_many(posts_data)
        post_ids = posts_result.inserted_ids
        print(f"✅ Created {len(post_ids)} posts")
        
        # Print summary
        print("\n📊 Database Seeding Summary:")
        print(f"   Users created: {len(user_ids)}")
        print(f"   Posts created: {len(post_ids)}")
        print("✅ Database seeding completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        return False

def verify_data():
    """Verify that data was inserted correctly"""
    print("\n🔍 Verifying seeded data...")
    
    db = get_db()
    
    # Count documents
    users_count = db.users.count_documents({})
    posts_count = db.posts.count_documents({})
    
    print(f"📈 Database Statistics:")
    print(f"   Total users: {users_count}")
    print(f"   Total posts: {posts_count}")
    
    # Show sample data
    print("\n👤 Sample Users:")
    for user in db.users.find().limit(3):
        print(f"   - {user['name']} ({user['email']})")
    
    print("\n📄 Sample Posts:")
    for post in db.posts.find().limit(3):
        print(f"   - {post['title']}")

if __name__ == "__main__":
    print("🚀 QR Food Database Seeder")
    print("=" * 40)
    
    success = seed_database()
    
    if success:
        verify_data()
        print("\n🎉 All done! Your database is ready to use.")
    else:
        print("\n❌ Seeding failed. Please check your MongoDB connection.")
