from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import router as analyzer_router

app = FastAPI()

# CORS (customize origin in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(analyzer_router, prefix="/analyze")
