from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv
import hashlib
from pydantic import BaseModel
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="URL Shortener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_url = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    clicks = Column(Integer, default=0)

@app.get("/health")
async def health_check():
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        result.first()
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

class URLBase(BaseModel):
    url: str
    custom_path: Optional[str] = None

class URLResponse(BaseModel):
    original_url: str
    short_url: str
    created_at: datetime
    clicks: int

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

def create_short_url(url: str, length: int = 7) -> str:
    hash_object = hashlib.sha256(url.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig[:length]

@app.post("/shorten", response_model=URLResponse)
async def create_short_url_endpoint(url_data: URLBase):
    db = SessionLocal()
    try:
        existing_url = db.query(URL).filter(URL.original_url == url_data.url).first()
        if existing_url:
            return URLResponse(
                original_url=existing_url.original_url,
                short_url=existing_url.short_url,
                created_at=existing_url.created_at,
                clicks=existing_url.clicks
            )
        
        short_path = url_data.custom_path or create_short_url(url_data.url)
        
        if url_data.custom_path and db.query(URL).filter(URL.short_url == short_path).first():
            raise HTTPException(status_code=400, detail="Custom URL already taken")
        
        db_url = URL(
            original_url=url_data.url,
            short_url=short_path,
            created_at=datetime.utcnow()
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        
        return URLResponse(
            original_url=db_url.original_url,
            short_url=db_url.short_url,
            created_at=db_url.created_at,
            clicks=db_url.clicks
        )
    finally:
        db.close()

@app.get("/{short_url}")
async def redirect_to_url(short_url: str):
    db = SessionLocal()
    try:
        db_url = db.query(URL).filter(URL.short_url == short_url).first()
        if not db_url:
            logger.warning(f"URL not found: {short_url}")
            raise HTTPException(status_code=404, detail="URL not found")
        
        db_url.clicks += 1
        db.commit()
        
        return RedirectResponse(url=db_url.original_url, status_code=302)
    finally:
        db.close()

@app.get("/stats/{short_url}")
async def get_url_stats(short_url: str):
    db = SessionLocal()
    try:
        db_url = db.query(URL).filter(URL.short_url == short_url).first()
        if not db_url:
            logger.warning(f"URL stats not found: {short_url}")
            raise HTTPException(status_code=404, detail="URL not found")
        
        return URLResponse(
            original_url=db_url.original_url,
            short_url=db_url.short_url,
            created_at=db_url.created_at,
            clicks=db_url.clicks
        )
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)