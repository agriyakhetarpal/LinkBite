---
title: LinkBite
emoji: ⚓
colorFrom: yellow
colorTo: red
sdk: docker
python_version: 3.9
app_file: gradio-app.py
language: 
  - en
tags:
- fastapi
- sqlalchemy
license: mit
---

![Logo for LinkBite](img/LinkBite.png)

# LinkBite 

LinkBite is a fast, minimalist URL shortener web app built for simplicity. It uses the `secrets` standard library for PRNG-based cryptographic tokens in Python (see [PEP 506](https://peps.python.org/pep-0506/) for more info).

LinkBite has a FastAPI + SQLite backend with SQLAlchemy ORM to connect the RESTful API endpoints to the database, and a Gradio frontend. This project also serves as a primer to FastAPI and its advanced functionalities.

## Features

- Create and manage your own shortened URLs
- Graceful forwarding: check if the URL exists
- Analytics: count the number of clicks on your URL
- Admin to deactivate shortened links (through a secret key to said links) 

# User setup

## Installation

It is recommended to install LinkBite within a Python [virtual environment](https://www.dataquest.io/blog/a-complete-guide-to-python-virtual-environments/). LinkBite has a minimal number of dependencies enlisted in **requirements.txt**. To install all of them, clone the repository and run

```
pip install -r requirements.txt
```

## Environment variables

LinkBite uses [`python-dotenv`](https://pypi.org/project/python-dotenv/) to build environment variables. To test your build, set your environment variables in a `.env` file in the install directory.

```
ENV_NAME="dev"
BASE_URL="http://localhost:8000"
DB_URL="sqlite:///./shortener.db"
```

## Web server

FastAPI leverages the ASGI standard to implement asynchronous event loops within a single process. For the web server; in the current directory, run

```
uvicorn shortener.main:app --reload
```

# API documentation

You can view all the API endpoints in FastAPI's autogenerated documentation at the base URL, i.e., https://localhost/8000/docs by default, or the alternative documentation at https://localhost/8000/redoc. The API methods have been defined in `shortener/main.py`.

# Tests
The tests are for the API endpoints currently and do not test Sessions' database operations. They are written with `starlette.testclient` and `pytest` located at `shortener/test_main.py`. To run the tests, start the server and simply run `pytest`.

# Frontend
LinkBite has a Gradio frontend connecting to the API endpoints with thin wrappers, inside `gradio-app.py`. The frontend can be run using
```
python gradio-app.py
```
or in reload mode using
```
gradio gradio-app.py
```
and then go to https://localhost:7860.

# Deployment

# Contributing
Improvements to the source code, documentation, feature requests, adding and improving tests, and catching and fixing bugs are all welcomed and appreciated – thanks! Please have a look at the issues or the source code. 

# License
MIT

# References
```
@software{Abid_Gradio_Hassle-free_sharing_2019,
author = {Abid, Abubakar and Abdalla, Ali and Abid, Ali and Khan, Dawood and Alfozan, Abdulrahman and Zou, James},
doi = {10.48550/arXiv.1906.02569},
month = {6},
title = {{Gradio: Hassle-free sharing and testing of ML models in the wild}},
url = {https://arxiv.org/abs/1906.02569},
year = {2019}
}
```