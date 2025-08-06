from fastapi import APIRouter
# from fastapi.responses import HTMLResponse

from oauth_google import generate_google_oauth_redirect_uri

router = APIRouter(prefix="/auth", tags=["oauth2_google"])


@router.get("/google/url")
async def get_google_oauth_redirect_iri() -> str:
    uri: str = generate_google_oauth_redirect_uri()
    return uri
