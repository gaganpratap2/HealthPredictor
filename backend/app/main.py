from fastapi import FastAPI

app = FastAPI(
    title="Patient Digital Twin API",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "patient-digital-twin"
    }