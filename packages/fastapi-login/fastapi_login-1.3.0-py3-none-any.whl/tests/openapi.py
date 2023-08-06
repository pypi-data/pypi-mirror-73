import uvicorn
from fastapi import FastAPI, Depends

from fastapi_login import LoginManager

app = FastAPI()
manager = LoginManager("secret", "/token")


@manager.user_loader
def load_user(_):
    return "Max-Rausch"


@app.get("/items/")
async def read_items(token: str = Depends(manager)):
    return {"token": token}


@app.post('/token')
def login():
    return {'access_token': manager.create_access_token(data={'sub': 'my-data'})}


if __name__ == '__main__':
    uvicorn.run(app)
