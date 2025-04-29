from fastapi import FastAPI, HTTPException, Depends, Header
from backend.models import UserLogin
from backend.auth import verify_password, create_token, decode_token
import duckdb
from backend.logger import log_access
from backend.logger import log_access, log_failed_login

app = FastAPI()
conn = duckdb.connect('users.db')


@app.post("/login")
def login(user: UserLogin):
    with duckdb.connect("backend/mydata.db") as conn:
        result = conn.execute(
            "SELECT password FROM users WHERE username = ?", (user.username,)
        ).fetchone()

        if result is None:
            log_failed_login(user.username)
            raise HTTPException(status_code=401, detail="Invalid username")

        if not verify_password(user.password, result[0]):
            log_failed_login(user.username)
            raise HTTPException(status_code=401, detail="Invalid password")

        log_access(user.username, "/login")  # log du login réussi
        return {"token": create_token({"sub": user.username})}






def auth_required(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()
        return decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/secure-data")
def secure_data(token: dict = Depends(auth_required)):
    log_access(token["sub"], "/secure-data")  # ⬅️ Ajout du logging ici
    return {"message": f"Hello {token['sub']}, your data is safe!"}

