import os
from main import app, db, create_tables

# Create database tables on first invocation
try:
    with app.app_context():
        create_tables()
except Exception as e:
    print(f"Database initialization warning: {e}")

# For Vercel serverless
handler = app.wsgi_app
