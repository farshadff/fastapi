from fastapi import FastAPI
from routers import api

app = FastAPI(debug=True)

app.include_router(api.router)

