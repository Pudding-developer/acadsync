from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import webbrowser
import os

# allows http redirection
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

APP_URL = "http://localhost:8000/api/credential-register"
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]


# opens a browser to allow user from accessing its google data
def get_browser_auth_url():
    flow = Flow.from_client_secrets_file(
        'backend/config/credentials.json',
        scopes=SCOPES,
        redirect_uri=APP_URL
    )

    auth_url, _ = flow.authorization_url(prompt='consent')
    return auth_url


# retrieves user credentials with the given api token
def get_user_credentials(api_link):
    flow = Flow.from_client_secrets_file(
        'config/credentials.json',
        scopes=SCOPES,
        redirect_uri=APP_URL
    )

    flow.fetch_token(authorization_response=api_link)
    creds = flow.credentials

    oauth2_service = build('oauth2', 'v2', credentials=creds)
    userinfo = oauth2_service.userinfo().get().execute()

    return {
        "name": userinfo.get("name"),
        "email": userinfo.get("email")
    }


# retrieves user' course
def get_user_courses(api_link):
    flow = Flow.from_client_secrets_file(
        'config/credentials.json',
        scopes=SCOPES,
        redirect_uri=APP_URL
    )

