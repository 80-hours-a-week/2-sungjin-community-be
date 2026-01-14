from __future__ import annotations

from fastapi.responses import JSONResponse
from app.common.responses import ok, created, bad_request, unauthorized, conflict, server_error
from app.models import users_model


def signup(payload: dict) -> JSONResponse:
    try:
        email = payload.get("email")
        password = payload.get("password")
        nickname = payload.get("nickname")

        if not email or not password or not nickname:
            return bad_request("missing_required_fields")

        if users_model.is_email_exists(email):
            return conflict("email_already_exists")

        if users_model.is_nickname_exists(nickname):
            return conflict("nickname_already_exists")

        users_model.create_user(email=email, password=password, nickname=nickname)
        return created("signup_success", None)

    except Exception:
        return server_error()


def login(payload: dict) -> JSONResponse:
    try:
        email = payload.get("email")
        password = payload.get("password")

        if not email or not password:
            return bad_request("missing_required_fields")

        user = users_model.find_user_by_email(email)
        if user is None:
            return unauthorized("email_not_found")

        if user["password"] != password:
            return unauthorized("wrong_password")

        token = users_model.create_session(user_id=user["id"])

        posts_preview = [
            {"post_id": 1, "title": "welcome", "author": user["nickname"]},
            {"post_id": 2, "title": "rules", "author": "admin"},
        ]

        data = {"access_token": token, "token_type": "bearer", "posts": posts_preview}
        return ok("login_success", data)

    except Exception:
        return server_error()


def logout(authorization: str | None) -> JSONResponse:
    try:
        if not authorization or not authorization.startswith("Bearer "):
            return unauthorized("unauthorized")

        token = authorization.split(" ", 1)[1].strip()

        user_id = users_model.get_user_id_by_token(token)
        if user_id is None:
            return unauthorized("invalid_token")

        users_model.delete_session(token)
        return ok("logout_success", None)

    except Exception:
        return server_error()
