from main import app

# For Vercel serverless
handler = app.wsgi_app
