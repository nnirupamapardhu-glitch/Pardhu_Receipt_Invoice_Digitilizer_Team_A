from fastapi import FastAPI
from app.db.session import engine, Base
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.invoice_routes import router as invoice_router
from app import models



app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables
Base.metadata.create_all(bind=engine)


# home route
@app.get("/")
def home():
    return {"message": "Server running"}

# auth router
app.include_router(auth_router)
app.include_router(invoice_router)
