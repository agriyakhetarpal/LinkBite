from fastapi import FastAPI, HTTPException
import validators

import schemas

app = FastAPI()

@app.get("/")
def read_root():
    return "API for LinkBite: the FastAPI-enabled URL shortener"
    
def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/url")
def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url):
        raise_bad_request(message="Invalid URL")
        # to be added
        return 