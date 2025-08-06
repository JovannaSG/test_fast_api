import urllib.parse

from config import settings


def generate_google_oauth_redirect_uri() -> str:
    query_params: dict = {
        "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": "http://localhost:8000/auth/google",
        "response_type": "code",
        "scope": " ".join([
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/calendar",
            "openid",
            "profile",
            "email"
        ]),
        # управляем scope, пока не пользователь не отзовет права
        "access_type": "offline"
        # state: ...
    }

    query_string: str = urllib.parse.urlencode(
        query_params,
        quote_via=urllib.parse.quote
    )
    base_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    return f"{base_url}?{query_string}"
