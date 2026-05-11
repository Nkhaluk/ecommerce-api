from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

USERS = {
    "admin": "1234",
    "ali": "password"
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):

    password = USERS.get(credentials.username)

    if password != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return credentials.username