import os

import firebase_admin
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials

_SERVICE_ACCOUNT_PATH = os.getenv(
    "FIREBASE_SERVICE_ACCOUNT", "secrets/serviceAccount.json"
)

if not firebase_admin._apps:
    firebase_admin.initialize_app(credentials.Certificate(_SERVICE_ACCOUNT_PATH))

_bearer = HTTPBearer(auto_error=True)


def verify_token(
    cred: HTTPAuthorizationCredentials = Depends(_bearer),
) -> dict:
    try:
        return auth.verify_id_token(cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
