from pydantic import BaseModel
from typing import List

class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config:
        from_attributes =  True
        # or 
        # orm_mode = True
'''Using orm_mode = True in Pydantic models allows FastAPI to serialize SQLAlchemy ORM model instances, 
ensuring data validation, proper JSON formatting, and automatic documentation generation.'''

class Blogupdate(BaseModel):
    title: str = None
    body: str = None

    class config:
        from_attributes = True