from fastapi import FastAPI

from app.routes.albums import router as albums_router

app = FastAPI(title="Albums API", version="1.0.0")
app.include_router(albums_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
