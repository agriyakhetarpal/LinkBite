from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse

import validators

from . import models, schemas, crud
from sqlalchemy.orm import Session
from .database import SessionLocal, engine


app = FastAPI()
# binds database engine created in database.py
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def not_found_error(request):
    message = f"This URL, {request.url} does not exist."
    raise HTTPException(status_code=404, detail=message)

@app.get("/")
def read_root():
    return "API for LinkBite: the FastAPI-enabled URL shortener"

@app.get("/{url_key}")
# called only when client URL matches host and key patterns
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
    ):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        not_found_error(request)
    
def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/url", response_model=schemas.URLInfo)
# to close session after finishing a request
def create_url(url: schemas.URLBase, db:Session = Depends(get_db)):
    # todo: try a regex-based approach to minimise dependencies
    if not validators.url(url.target_url):
        raise_bad_request(message="Invalid URL")

    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key
    
    return db_url 