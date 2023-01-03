from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
import requests

import validators
from starlette.datastructures import URL

from . import models, schemas, crud
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .config import get_settings


app = FastAPI()
# binds database engine created in database.py
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def not_found_error_internal(request):
    message = f"This URL, {request.url} does not exist."
    raise HTTPException(status_code=404, detail=message)


@app.get("/")
def read_root():
    return "LinkBite: the FastAPI-enabled URL shortener"


@app.get("/{url_key}")
# called only when client URL matches host and key patterns
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        not_found_error_internal(request)


@app.get("/peek/{url_key}")
# to get URL from database whose shortened URL is known
def peek_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = crud.get_db_url_by_key(db=db, url_key=url_key)
    if db_url is None:
        raise not_found_error_internal(request)
    return {db_url.target_url}


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_404(message):
    raise HTTPException(status_code=404, detail=message)


@app.get("/admin/{secret_key}", name="Admin panel", response_model=schemas.URLInfo)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        not_found_error_internal(request)


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for("Admin panel", secret_key=db_url.secret_key)
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@app.post("/url", response_model=schemas.URLInfo)
# to close session after finishing a request
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    # todo: try a regex-based approach to minimise dependencies
    if not validators.url(url.target_url):
        raise_bad_request(message="Invalid URL")
    # graceful forwarding: if URL does not exist
    try:
        response = requests.head(url.target_url)
        if response.status_code == 404:
            raise_404(message="This URL does not exist")
    except requests.RequestException:
        raise_bad_request(message="Error accessing URL")

    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.deactivate_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted your shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        not_found_error_internal(request)
