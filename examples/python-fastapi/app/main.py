from fastapi import FastAPI

app = FastAPI(title="MTS FastAPI Demo")


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello from MTS FastAPI"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

