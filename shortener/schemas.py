from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str

class URL(URLBase):
    is_active: bool
    # count number of visits for shortened URL
    clicks: int
    # allow manual tags for a URL
    tags: str

    class Config:
        # for SQLAlchemy
        orm_mode = True
    
class URLInfo(URL):
    url: str
    admin_url: str