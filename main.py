from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic_models import UserCreate, UserOut, UserLogin
import uuid
from passlib.context import CryptContext
from database import SessionLocal, User
from datetime import datetime, timezone

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- DB dependency ---
def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()


@app.get("/")
def root():
    return ("Mental Health AI assistant is running...")


# --- Sign up ---
@app.post("/users/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered, try signing in...")

    hashed = pwd_context.hash(user.password)

    new_user = User( 
        name = user.name,
        email = user.email,
        password = hashed,
        created_at = datetime.now(timezone.utc)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserOut(
        id = new_user.id,
        name = new_user.name,
        email = new_user.email,
        created_at = new_user.created_at
    )


# --- Login ---
@app.post("/users/login", response_model=UserOut)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return UserOut(
        id = db_user.id,
        name = db_user.name,
        email = db_user.email,
        created_at = db_user.created_at
    )


# --- Account delete ---
@app.delete("/users")
def delete_user(email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    if not pwd_context.verify(password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    db.delete(db_user)
    db.commit()

    return {"detail": f"{email} deleted successfully"}
