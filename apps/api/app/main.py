from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter
from app.core.config import settings
from app.api.routes import analyses, health, profiles, change_reviews
from app.db.models import Base
from app.db.session import engine

app = FastAPI(title="ChainTrust API", version="0.1.0", description="Evidence-aware smart contract release and risk intelligence for Sepolia engineering review workflows.")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins.split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(health.router)
app.include_router(analyses.router)
app.include_router(profiles.router)
app.include_router(change_reviews.router)
@app.on_event("startup")
def create_tables(): Base.metadata.create_all(bind=engine)
