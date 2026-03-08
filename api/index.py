import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import app
    
    # Initialize database on first request
    @app.before_request
    def init_db():
        if not hasattr(app, '_db_initialized'):
            try:
                from main import db, create_tables
                with app.app_context():
                    create_tables()
                app._db_initialized = True
            except Exception as e:
                print(f"Database init error: {e}")
                
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    raise

# Export for Vercel
handler = app.wsgi_app
