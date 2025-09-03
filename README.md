# QR Food Backend

A Flask backend API with MongoDB integration for managing users and posts.

## Features

- RESTful API endpoints
- MongoDB database integration
- CORS enabled for frontend integration
- JSON responses with consistent structure
- Basic error handling and validation
- Health check endpoint with database status
- Unique email validation for users
- Database seeding script

## Prerequisites

- Python 3.7+
- MongoDB (local installation or MongoDB Atlas account)

## MongoDB Setup

### Option 1: Local MongoDB
1. Download and install MongoDB from [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
2. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # macOS (with Homebrew)
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   ```

### Option 2: MongoDB Atlas (Cloud)
1. Create a free account at [https://www.mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get your connection string
4. Update the `MONGO_URI` in your environment configuration

## Installation

1. Clone the repository and navigate to the project folders
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
4. Update the `.env` file with your MongoDB configuration

## Database Setup

Seed the database with initial data:
```bash
python seed_database.py
```

## Running the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### General
- `GET /` - Welcome message with API documentation
- `GET /health` - Health check endpoint (includes database status)

### Users
- `GET /users` - Get all users
- `GET /users/<id>` - Get user by MongoDB ObjectId
- `POST /users` - Create a new user (email must be unique)

### Posts
- `GET /posts` - Get all posts
- `GET /posts/<id>` - Get post by MongoDB ObjectId
- `POST /posts` - Create a new post

## API Usage Examples

### Create a User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "email": "alice@example.com"}'
```

### Get All Users
```bash
curl http://localhost:5000/users
```

### Create a Post
```bash
curl -X POST http://localhost:5000/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My New Post", "content": "This is my post content", "author_id": "USER_OBJECT_ID_HERE"}'
```

### Get All Posts
```bash
curl http://localhost:5000/posts
```

## Testing the API

Run the included test script:
```bash
python test_api.py
```

## Response Format

All API responses follow this structure:

```json
{
  "success": true|false,
  "data": {...},  // Present on success
  "error": "...", // Present on error
  "message": "..." // Optional message
}
```

## MongoDB Document Structure

### Users Collection
```json
{
  "_id": ObjectId,
  "name": "string",
  "email": "string (unique)",
  "created_at": "ISO datetime string"
}
```

### Posts Collection
```json
{
  "_id": ObjectId,
  "title": "string",
  "content": "string", 
  "author_id": "string (User ObjectId)",
  "created_at": "ISO datetime string"
}
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=qrfood_db
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

## Development

The application runs in debug mode by default, which means:
- Automatic reloading when code changes
- Detailed error messages
- Development server warnings

For production, make sure to:
- Set `FLASK_ENV=production`
- Use a secure `SECRET_KEY`
- Use a proper WSGI server like Gunicorn
- Set `debug=False` in the Flask app

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running on your system
- Check that the `MONGO_URI` in your `.env` file is correct
- For MongoDB Atlas, ensure your IP is whitelisted and credentials are correct

### Common Errors
- **"User not found"**: Make sure to use valid MongoDB ObjectId format
- **"Email already exists"**: User emails must be unique
- **Database connection failed**: Check MongoDB service status
