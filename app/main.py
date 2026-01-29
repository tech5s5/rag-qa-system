from fastapi import FastAPI
from app.api import router
from app.rate_limiter import limiter
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(title="RAG QA System")

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(router)
