import secrets

from sqlalchemy.orm import Session
from . import crud


def create_key(length: int = 5) -> str:
    chars = "".join([chr(i) for i in range(65, 91)]) + "".join(
        [chr(i) for i in range(48, 58)]
    )
    return "".join(secrets.choice(chars) for _ in range(length))


# repeat until key is unique by iterating over all existing keys
def create_unique_key(db: Session) -> str:
    key = create_key()
    while crud.get_db_url_by_key(db, key):
        key = create_key()
    return key
