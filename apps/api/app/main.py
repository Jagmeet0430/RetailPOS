from fastapi import FastAPI

app = FastAPI(
    title="RetailPOS API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "RetailPOS API",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
