# Flask Google OAuth App - Deployment Guide

This Flask application integrates Google OAuth for authentication and Google Sheets for data storage.

## Prerequisites

1. **Google Cloud Console Setup:**
   - Create a project at [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Google OAuth 2.0 API and Google Sheets API
   - Create OAuth 2.0 credentials (Web Application)
   - Create a Service Account and download the JSON key file
   - Share your Google Sheet with the service account email

2. **Required Files:**
   - `credentials.json` (OAuth credentials from Google Cloud Console)
   - `service_account.json` (Service account key from Google Cloud Console)

## Easy Deployment Options

### 1. **Render (Recommended - Free Tier Available)**

1. Fork/upload your code to GitHub
2. Go to [Render](https://render.com) and connect your GitHub account
3. Create a new Web Service
4. Configure environment variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-super-secret-key-here
   REDIRECT_URI=https://your-app-name.onrender.com/callback
   SPREADSHEET_ID=your-google-sheet-id
   ```
5. Upload your JSON files as secrets or environment variables
6. Deploy!

**Pros:** Free tier, automatic deployments, easy setup
**Cons:** Cold starts on free tier

### 2. **Railway**

1. Go to [Railway](https://railway.app)
2. Connect your GitHub repository
3. Set environment variables in the Railway dashboard
4. Add your JSON credentials as environment variables
5. Deploy automatically

**Pros:** Fast deployments, good free tier
**Cons:** Limited free usage

### 3. **Heroku**

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Run these commands:
   ```bash
   heroku create your-app-name
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set REDIRECT_URI=https://your-app-name.herokuapp.com/callback
   heroku config:set SPREADSHEET_ID=your-sheet-id
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

**Pros:** Mature platform, lots of add-ons
**Cons:** No free tier anymore

### 4. **PythonAnywhere**

1. Upload your files to PythonAnywhere
2. Set up a web app using Flask
3. Configure environment variables in the web app settings
4. Upload your JSON files to the files section

**Pros:** Simple setup, good for beginners
**Cons:** Limited on free tier

### 5. **Vercel**

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your project directory
3. Configure environment variables in the Vercel dashboard

**Pros:** Great performance, easy deployment
**Cons:** Serverless limitations

## Environment Variables Setup

Create a `.env` file (for local development) with these variables:

```env
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here
REDIRECT_URI=http://127.0.0.1:5000/callback
SPREADSHEET_ID=your-google-sheet-id
PORT=5000
```

For production, set these in your hosting platform's environment variables section.

## Google OAuth Setup Steps

1. **Google Cloud Console:**
   - Go to APIs & Services > Credentials
   - Create OAuth 2.0 Client ID (Web Application)
   - Add your domain to authorized origins
   - Add your callback URL to authorized redirect URIs

2. **Service Account:**
   - Create a service account
   - Download the JSON key file
   - Share your Google Sheet with the service account email

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. Run the app:
   ```bash
   python app.py
   ```

## Security Notes

- Never commit `credentials.json`, `service_account.json`, or `.env` files to version control
- Use strong secret keys in production
- Always use HTTPS in production
- Regularly rotate your API keys

## Troubleshooting

- **OAuth Error:** Check that your redirect URI matches exactly in Google Cloud Console
- **Sheets Error:** Ensure the service account has access to your Google Sheet
- **Environment Variables:** Double-check all environment variables are set correctly
- **Dependencies:** Make sure all packages in requirements.txt are installed

## Quick Start Commands

```bash
# Install missing dependencies
pip install google-auth google-auth-oauthlib google-api-python-client gspread python-dotenv gunicorn

# Test locally
python app.py

# Deploy to Render/Railway (after pushing to GitHub)
# Just connect your repo in their dashboard!
```