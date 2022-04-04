from flask import Blueprint, request, Response
from models import User
from orjson import dumps

router = Blueprint("users", __name__, url_prefix="/users")


@router.get("/")
def get_users():
    all_users = User.query.all()
    return Response(dumps(all_users), mimetype="application/json", status=200)


@router.get("/{id}")
def get_user(id: str):
    user = User.query.filter_by(id=id).first_or_404()
    return Response(dumps(user), mimetype="application/json", status=200)


@router.post("/")
def create_user():
    data = request.get_json()
    user = User(**data)
    user.save()
    return Response(dumps(user), mimetype="application/json", status=201)


@router.put("/{id}")
def update_user(id: str):
    data = request.get_json()
    user = User.query.filter_by(id=id).first_or_404()
    user.update(**data)
    return Response(dumps(user), mimetype="application/json", status=200)


@router.delete("/{id}")
def delete_user(id: str):
    user = User.query.filter_by(id=id).first_or_404()
    user.delete()
    return Response(status=204)
