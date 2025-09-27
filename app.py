import os
import gspread
from flask import Flask, redirect, url_for, session, request, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
# This secret key is needed for session management
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# --- Google Sheets Configuration ---
# You need to share your Google Sheet with the client_email in your service_account.json
# The scope defines the permissions your app is requesting.
GSHEET_SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'service_account.json'
# The ID of your spreadsheet
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', '1zdZqSqREyTcMpaHytd49ISS43mBOMHVmBR0JlJEXRvM')

# Authenticate with Google Sheets using the service account
try:
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.sheet1
    print("Successfully connected to Google Sheets.")
except Exception as e:
    print(f"Error connecting to Google Sheets: {e}")
    worksheet = None

# --- Google OAuth 2.0 Configuration ---
# This file contains your client ID and client secret.
CLIENT_SECRETS_FILE = "credentials.json"
# This scope allows us to see user's profile info
OAUTH_SCOPE = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]
# The URL your users will be sent back to after they log in.
# It must match what you've set in the Google Cloud Console.
REDIRECT_URI = os.environ.get('REDIRECT_URI', "http://127.0.0.1:5000/callback")

# --- Flask Routes ---

@app.route("/")
def index():
    """Renders the login page."""
    return render_template("login.html")

@app.route("/login")
def login():
    """Redirects the user to Google's authentication page."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=OAUTH_SCOPE,
        redirect_uri=REDIRECT_URI
    )
    # The authorization_url is the link to Google's sign-in page.
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    """Handles the callback from Google after user authentication."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=OAUTH_SCOPE,
        state=session['state'],
        redirect_uri=REDIRECT_URI
    )
    # This exchanges the authorization code for an access token.
    flow.fetch_token(authorization_response=request.url)
    
    # Store the credentials in the session.
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    # Use the token to get user info
    from googleapiclient.discovery import build
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    # Store user info in session
    session['user_info'] = user_info

    return redirect(url_for("home"))

@app.route("/home")
def home():
    """Displays the home page with the form if the user is logged in."""
    if 'credentials' not in session:
        return redirect(url_for("index"))

    user_info = session.get('user_info', {})
    return render_template("home.html", user_info=user_info)

@app.route("/submit", methods=["POST"])
def submit():
    """Handles form submission and writes data to Google Sheets."""
    if 'credentials' not in session:
        return redirect(url_for("index"))

    if worksheet is None:
        return "Error: Could not connect to the Google Sheet. Please check server logs.", 500

    try:
        name = request.form.get("name")
        pincode = request.form.get("pincode")
        
        user_email = session.get('user_info', {}).get('email', 'N/A')

        worksheet.append_row([name, pincode, user_email])
        
        return redirect(url_for("success"))
    except Exception as e:
        print(f"Error writing to sheet: {e}")
        return f"An error occurred while submitting your data: {e}", 500

@app.route("/success")
def success():
    """Displays a success message."""
    return render_template("success.html")

@app.route("/logout")
def logout():
    """Logs the user out by clearing the session."""
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Only allow insecure transport in development
    if os.environ.get('FLASK_ENV') != 'production':
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
