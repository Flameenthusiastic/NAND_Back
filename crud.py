from fastapi import HTTPException, status
from uuid import uuid4
from firebase import db


async def get_all_users():
    docs = db.collection("users").stream()
    data = []
    for doc in docs:
        post = {"id": doc.id, **doc.to_dict()}
        data.append(post)
    return data


async def get_user(user_uuid: str):
    docs = db.collection("users").where("user_uuid", "==", user_uuid).stream()
    data = []
    for doc in docs:
        post = {"id": doc.id, **doc.to_dict()}
        data.append(post)
    return data


async def get_history(uuid: str):
    docs = db.collection("histories").where("uuid", "==", uuid).stream()
    data = []
    for doc in docs:
        post = {"id": doc.id, **doc.to_dict()}
        data.append(post)
    return data

async def get_history_related_user(user_uuid: str):
    docs = db.collection("histories").where("user_uuid", "==", user_uuid).stream()
    data = []
    for doc in docs:
        post = {"id": doc.id, **doc.to_dict()}
        data.append(post)
    print(data)
    return data


async def create_user(name: str) -> str:
    user_uuid = str(uuid4())
    doc_ref = db.collection("users").document()
    doc_ref.set({
        "user_uuid":user_uuid,
        "name": name,
    })
    return user_uuid


async def create_history(user_uuid: str, area: str, city: str, restaurant: str, hotel: str):
    uuid = str(uuid4())
    doc_ref = db.collection("histories").document()
    doc_ref.set({
        "user_uuid": user_uuid,
        "uuid": uuid,
        "area": area,
        "city": city,
        "restaurant": restaurant,
        "hotel": hotel
    })
    return uuid


async def update_user(user_uuid: str, name: str):
    docs = db.collection("users").where("user_uuid", "==", user_uuid).stream()
    data = []
    for doc in docs:
        post = {"id": doc.id, **doc.to_dict()}
        data.append(post)
    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="あなたのIDが見つかりませんでした")
    doc_ref = db.collection("users").document(data[0]["id"])
    doc_ref.update({"name": name})
    return name



