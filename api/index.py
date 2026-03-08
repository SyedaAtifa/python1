import sys
import os

# Ensure parent directory is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    # Import Flask app directly
    from main import app
    
    # Vercel WSGI handler
    def handler(environ, start_response):
        return app.wsgi_app(environ, start_response)
    
except ImportError as e:
    print(f"Fatal import error: {e}")
    import traceback
    traceback.print_exc()
    
    # Fallback minimal app if import fails
    def handler(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return [b'Failed to import app']
