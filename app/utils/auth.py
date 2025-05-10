import requests
from fastapi import HTTPException
from app.core.config import settings

async def verify_password_firebase(email: str, password: str) -> dict:
    """
    Verify user credentials against Firebase Auth REST API
    Returns the Firebase auth tokens if successful
    """
    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.FIREBASE_WEB_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            error_data = response.json()
            error_message = error_data.get('error', {}).get('message', 'Invalid credentials')
            raise HTTPException(status_code=401, detail=error_message)
        raise HTTPException(status_code=500, detail="Authentication service error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def verify_firebase_token(token: str) -> dict:
    """
    Verify Firebase ID token
    Returns the decoded token if valid
    """
    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={settings.FIREBASE_WEB_API_KEY}"
        payload = {"idToken": token}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def refresh_firebase_token(refresh_token: str) -> dict:
    """
    Refresh Firebase auth tokens using a refresh token
    Returns new set of tokens if successful
    """
    try:
        url = f"https://securetoken.googleapis.com/v1/token?key={settings.FIREBASE_WEB_API_KEY}"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 