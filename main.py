import json
from fastapi import FastAPI, Form, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import crud


app = FastAPI()

origins = [
    "http://localhost:5501"
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
async def get_users():
    users = await crud.get_all_users()
    resp = {
        "status": "ok", 
        "count": len(users), 
        "data": users
    }
    return resp


@app.get("/user")
async def get_user(uuid: str = Form(...)):
    user = await crud.get_user(uuid)
    resp = {
        "status": "ok",
        "data": user 
    }
    return resp


@app.get("/history")
async def get_history(uuid: str = Form(...)):
    history = await crud.get_history(uuid)
    resp = {
        "status": "ok",
        "data": history 
    }
    return resp


# 投稿機能を作る
@app.post("/user")
async def post(name: str = Form(...)):
    uuid = await crud.create_user(name)
    return JSONResponse(content={"status": "ok", "uuid": uuid, "name": name}, status_code=status.HTTP_201_CREATED)


@app.post("/history")
async def post(
    area: str = Form(...),
    district: str = Form(...),
    restaurant: str = Form(...),
    hotel: str = Form(...)
    ):
    uuid = await crud.create_history(area, district, restaurant, hotel)
    return JSONResponse(content={
        "status": "ok",
        "uuid": uuid,
        "area":area,
        "district":district,
        "restaurant":restaurant,
        "hotel":hotel
        }, status_code=status.HTTP_201_CREATED)


@app.put("/user")
async def put(uuid: str = Form(...), name: str = Form(...)):
    name = await crud.update_user(uuid, name)
    return JSONResponse(content={"status": "ok", "uuid": uuid, "name": name}, status_code=status.HTTP_200_OK)


# 起動
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
    