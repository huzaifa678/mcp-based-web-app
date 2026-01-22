from fastapi.params import Header
import jwt
from requests import Session
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from sqllite.users_db import SessionLocal, User
from tools.analyzer import analyze_code
from tools.advisor import advise_on_code
from pydantic import BaseModel

from utils.password import hash_password, verify_password
from utils.jwt_token import ALGORITHM, SECRET_KEY, create_access_token, create_refresh_token, verify_access_token

app = FastAPI()
mcp = FastMCP(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    
class RefreshRequest(BaseModel):
    refresh_token: str

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    register a new user"""
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created"}

@app.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    """
    login user and return access and refresh tokens
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_access_token({"sub": db_user.username})
    refresh = create_refresh_token({"sub": db_user.username})
    return {"access_token": access, "refresh_token": refresh}

@app.post("/renew", response_model=Token)
def refresh_token(request: RefreshRequest):
    """
    renew access and refresh tokens using a valid refresh token
    """
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        access = create_access_token({"sub": username})
        refresh = create_refresh_token({"sub": username})
        return {"access_token": access, "refresh_token": refresh}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@mcp.tool()
def analyze(code: str, authorization: str = Header(...)) -> list[TextContent]:
    """
    Analyze the given Python code and return feedback.
    """
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    static_feedback = analyze_code(code)
    ai_feedback = advise_on_code(code)

    combined = "\n".join([
        f"{item['message']}" for item in static_feedback + ai_feedback
    ])

    return [TextContent(type="text", text=combined)]

class CodeRequest(BaseModel):
    code: str

@app.post("/analyze")
def analyze_endpoint(request: CodeRequest, http_request: Request):
    
    auth_header = http_request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    static_feedback = analyze_code(request.code)
    ai_feedback = advise_on_code(request.code)
    
    static_feedback_list = [{"type": "static", "message": f["message"]} for f in static_feedback]
    ai_feedback_list = [{"type": "ai", "message": f["message"]} for f in ai_feedback]
    
    return {
        "static": static_feedback_list,
        "ai": ai_feedback_list
    }

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
