from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "API for LinkBite: the FastAPI-enabled URL shortener"