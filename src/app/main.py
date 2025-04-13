from fastapi import FastAPI
from src.app.api import routes


app = FastAPI(
    title="Equal Weighted Index API",
    version="1.0.0",
    description="API for computing and retrieving a custom equal-weighted index."
)

# Register routes
app.include_router(routes.router)


# Optional health check
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}
