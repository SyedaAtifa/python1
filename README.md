# Career Advice Boat

This is a simple Flask application that helps users discover career advice based on their interests. The project has been enhanced with user accounts, a database, dynamic interests, and AJAX.

## Features

- User registration and login (Flask‑Login, Flask‑WTF)
- Persists data using SQLite (SQLAlchemy)
- Dynamic list of interests loaded from database
- Advice can be stored in the database or in an external JSON file (`advice_data.json`)
- Users can submit new interests and advice suggestions
- Ratings collect feedback and influence which advice is shown first
- AJAX endpoint (`/api/advice`) for fetching advice without reloading the page
- Clean UI with CSS and navigation

## Getting Started

1. Create a virtual environment and install dependencies:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   pip install -r requirements.txt
   ```
2. Run the application:
   ```powershell
   python main.py
   ```
3. Visit http://localhost:5000 in your browser.

## Database

The app uses SQLite (`career.db`) and will create tables automatically on first request. Default interests and advice are seeded from `advice_data.json`.

## Configuration

Set `SECRET_KEY` environment variable for production. You can also change the database URI via `SQLALCHEMY_DATABASE_URI`.

## Development Tips

- `templates/base.html` is the layout; other pages extend it.
- Add new advice or interests via the web interface once logged in.
- You can extend the models in `models/` to add more fields.

Happy coding!

## Deploying on Vercel

Vercel can host the app using a Docker container. Create a `Dockerfile` (included in this repo) and a simple `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    { "src": "Dockerfile", "use": "@vercel/docker" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/" }
  ]
}
```

Then from the project directory:

```bash
vercel login
vercel --prod
``` 

The build will containerize your app and run it on Vercel’s infrastructure. Set environment variables (`SECRET_KEY`, `SQLALCHEMY_DATABASE_URI` etc.) in the Vercel dashboard or with `vercel env add`.

You can also deploy using Vercel's GitHub integration: push to a repo and connect it in the Vercel dashboard; configure the project to use the Dockerfile build step.

Alternatively, if you prefer not to use Docker, Vercel supports Python serverless functions, but container approach is simpler for a full‑Flask app.
