import json
from fastapi import FastAPI, Form, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import crud


app = FastAPI()

origins = [
    "http://localhost:5501",
    "http://127.0.0.1:5501/",
    "https://nand-application.herokuapp.com",
    "https://nand-e7173.web.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ルート
@app.get("/")
async def root():
    return {"message": "this is root"}


@app.get("/users")
async def get_all_users():
    users = await crud.get_all_users()
    resp = {
        "status": "ok", 
        "count": len(users), 
        "data": users
    }
    return resp


@app.get("/user")
async def get_user(user_uuid: str):
    user = await crud.get_user(user_uuid)
    resp = {
        "status": "ok",
        "data": user 
    }
    return resp


@app.get("/history")
async def get_history(uuid: str):
    history = await crud.get_history(uuid)
    resp = {
        "status": "ok",
        "data": history 
    }
    return resp

@app.get("/history-related-user")
async def get_history_related_user(user_uuid: str):
    histories = await crud.get_history_related_user(user_uuid)
    resp = {
        "status": "ok",
        "count": len(histories),
        "data": histories
    }
    return resp


# 投稿機能を作る
@app.post("/user")
async def post(name: str = Form(...)):
    user_uuid = await crud.create_user(name)
    return JSONResponse(content={"status": "ok", "user_uuid": user_uuid, "name": name}, status_code=status.HTTP_201_CREATED)


@app.post("/history")
async def post(
    user_uuid: str = Form(...),
    area: str = Form(...),
    city: str = Form(...),
    restaurant: str = Form(...),
    hotel: str = Form(...)
    ):
    uuid = await crud.create_history(user_uuid, area, city, restaurant, hotel)
    return JSONResponse(content={
        "status": "ok",
        "user_uuid": user_uuid,
        "uuid": uuid,
        "area":area,
        "city":city,
        "restaurant":restaurant,
        "hotel":hotel
        }, status_code=status.HTTP_201_CREATED)


@app.put("/user")
async def put(user_uuid: str = Form(...), name: str = Form(...)):
    name = await crud.update_user(user_uuid, name)
    return JSONResponse(content={"status": "ok", "user_uuid": user_uuid, "name": name}, status_code=status.HTTP_200_OK)


# 起動
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
    