from fastapi import FastAPI, Body, Depends, status, Response, HTTPException
from typing import Annotated
from . import schemas
from sqlalchemy.orm import session, Session


from .database import Base, engine, SessionLocal
from . import models
from .models import Blog

Base.metadata.create_all(engine)
'''migrating the tables all the time if table
 is there update the tabel if not create the tabel'''

app = FastAPI()

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    '''or
    new _blog = models.Blog(**request.model_dump())'''

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog
''' -> this will be return as json because of orm_mode = True'''


@app.get('/blog')
def all(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs

'''on response the sqlalchemy model is converted into the pydantic model due to 
orm_mode and the pydantic serialize this pydantic instance to json automatically '''

@app.get('/blog/{id}',status_code= status.HTTP_200_OK )
def blogById(id: int,response: Response, db: Session = Depends(get_db)):  #parameter with default should be at the last
    blog = db.query(models.Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Blog with id {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return ({'detain': f"Blog with id {id} is not found"})
    return blog


@app.delete('/blog/{id}', status_code= status.HTTP_204_NO_CONTENT)  #this status code will be set to default
def destroy(id :int, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(Blog.id == id).delete(synchronize_session=False)

    db.commit()
    return {"done"}

@app.put('/blog/{id}')
def update(id:int,request: schemas.Blogupdate, db:Session = Depends(get_db)):
    update_model = {}

    blog = db.query(models.Blog).filter(Blog.id == id)
    if blog is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"the blog with id {id} is not found")
    
    if request.title is not None:
        update_model[Blog.title] = request.title
    if request.body is not None:
        update_model[Blog.body] = request.body

    blog.update(update_model)
    db.commit()

    return "done"






'''
Key Differences
Performance: Using synchronize_session='fetch' will add an extra query to fetch the primary keys of the affected rows, which can affect performance, especially with large datasets. Using synchronize_session=False skips this step, making it more efficient.

Session State: With synchronize_session='fetch', the session will be accurately synchronized with the database, ensuring the session's state matches the database state. With synchronize_session=False, the session might contain stale data until it is expired or refreshed.

Practical Impact
If you do not need to access the deleted objects after deletion, synchronize_session=False is usually the best choice as it improves performance.
If you need to ensure the session's state is up-to-date with the database, use synchronize_session='fetch' or synchronize_session='evaluate' (with simpler queries).
In summary, the choice of synchronize_session parameter depends on your specific use case and the need for session synchronization accuracy versus performance.
'''


