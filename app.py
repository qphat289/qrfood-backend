from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json
from bson import ObjectId
from bson.errors import InvalidId
from database import get_db, init_database

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Helper function to convert ObjectId to string for JSON serialization
def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        doc = dict(doc)
        if '_id' in doc:
            doc['id'] = str(doc['_id'])
            del doc['_id']
        return doc
    return doc

# Helper function to find user by id
def find_user_by_id(user_id):
    """Find user by ObjectId or string ID"""
    try:
        db = get_db()
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        user = db.users.find_one({"_id": user_id})
        return serialize_doc(user)
    except (InvalidId, Exception):
        return None

# Helper function to find post by id
def find_post_by_id(post_id):
    """Find post by ObjectId or string ID"""
    try:
        db = get_db()
        if isinstance(post_id, str):
            post_id = ObjectId(post_id)
        post = db.posts.find_one({"_id": post_id})
        return serialize_doc(post)
    except (InvalidId, Exception):
        return None

# Routes

@app.route('/')
def home():
    """Welcome endpoint"""
    return jsonify({
        "message": "Welcome to the Flask Backend API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This welcome message",
            "GET /users": "Get all users",
            "GET /users/<id>": "Get user by ID",
            "POST /users": "Create a new user",
            "GET /posts": "Get all posts",
            "GET /posts/<id>": "Get post by ID",
            "POST /posts": "Create a new post",
            "GET /health": "Health check"
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db = get_db()
        db.command('ping')
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    
    return jsonify({
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    })

# User endpoints
@app.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        db = get_db()
        users_cursor = db.users.find()
        users_list = [serialize_doc(user) for user in users_cursor]
        
        return jsonify({
            "success": True,
            "data": users_list,
            "count": len(users_list)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = find_user_by_id(user_id)
    if user:
        return jsonify({
            "success": True,
            "data": user
        })
    else:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Basic validation
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({
                "success": False,
                "error": "Name and email are required"
            }), 400
        
        db = get_db()
        
        # Check if email already exists
        existing_user = db.users.find_one({"email": data["email"]})
        if existing_user:
            return jsonify({
                "success": False,
                "error": "Email already exists"
            }), 400
        
        new_user = {
            "name": data["name"],
            "email": data["email"],
            "created_at": datetime.now().isoformat() + "Z"
        }
        
        # Insert into MongoDB
        result = db.users.insert_one(new_user)
        new_user['id'] = str(result.inserted_id)
        
        return jsonify({
            "success": True,
            "message": "User created successfully",
            "data": new_user
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Post endpoints
@app.route('/posts', methods=['GET'])
def get_posts():
    """Get all posts"""
    try:
        db = get_db()
        posts_cursor = db.posts.find()
        posts_list = [serialize_doc(post) for post in posts_cursor]
        
        return jsonify({
            "success": True,
            "data": posts_list,
            "count": len(posts_list)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    """Get post by ID"""
    post = find_post_by_id(post_id)
    if post:
        return jsonify({
            "success": True,
            "data": post
        })
    else:
        return jsonify({
            "success": False,
            "error": "Post not found"
        }), 404

@app.route('/posts', methods=['POST'])
def create_post():
    """Create a new post"""
    try:
        data = request.get_json()
        
        # Basic validation
        if not data or 'title' not in data or 'content' not in data or 'author_id' not in data:
            return jsonify({
                "success": False,
                "error": "Title, content, and author_id are required"
            }), 400
        
        # Check if author exists
        author = find_user_by_id(data["author_id"])
        if not author:
            return jsonify({
                "success": False,
                "error": "Author not found"
            }), 400
        
        db = get_db()
        
        new_post = {
            "title": data["title"],
            "content": data["content"],
            "author_id": data["author_id"],
            "created_at": datetime.now().isoformat() + "Z"
        }
        
        # Insert into MongoDB
        result = db.posts.insert_one(new_post)
        new_post['id'] = str(result.inserted_id)
        
        return jsonify({
            "success": True,
            "message": "Post created successfully",
            "data": new_post
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    
    # Initialize database connection
    if not init_database():
        print("❌ Failed to connect to MongoDB. Please make sure MongoDB is running.")
        print("💡 You can start MongoDB locally or use MongoDB Atlas (cloud)")
        exit(1)
    
    print("API endpoints:")
    print("  GET  / - Welcome message")
    print("  GET  /health - Health check")
    print("  GET  /users - Get all users")
    print("  GET  /users/<id> - Get user by ID")
    print("  POST /users - Create user")
    print("  GET  /posts - Get all posts")
    print("  GET  /posts/<id> - Get post by ID")
    print("  POST /posts - Create post")
    print("\nServer running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
