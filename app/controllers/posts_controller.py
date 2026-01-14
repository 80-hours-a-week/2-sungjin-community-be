from __future__ import annotations

from fastapi.responses import JSONResponse
from app.common.responses import ok, created, bad_request, unauthorized, not_found, forbidden, server_error
from app.models import posts_model, users_model


def _require_user_id(authorization: str | None) -> int | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1].strip()
    return users_model.get_user_id_by_token(token)


def list_posts(authorization: str | None, page: int = 1, limit: int = 10) -> JSONResponse:
    try:
        user_id = _require_user_id(authorization)
        if user_id is None:
            return unauthorized("invalid_token")

        if page < 1 or limit < 1 or limit > 50:
            return bad_request("invalid_paging_params")

        posts = posts_model.list_posts(page=page, limit=limit)
        return ok("read_posts_success", {"items": posts, "page": page, "limit": limit})

    except Exception:
        return server_error()


def get_post_detail(authorization: str | None, post_id: int) -> JSONResponse:
    try:
        user_id = _require_user_id(authorization)
        if user_id is None:
            return unauthorized("invalid_token")

        post = posts_model.find_post(post_id)
        if post is None:
            return not_found("post_not_found")

        return ok("read_post_success", post)

    except Exception:
        return server_error()


def create_post(authorization: str | None, payload: dict) -> JSONResponse:
    try:
        user_id = _require_user_id(authorization)
        if user_id is None:
            return unauthorized("invalid_token")

        title = payload.get("title")
        content = payload.get("content")
        image_url = payload.get("image_url")

        if not title or not content:
            return bad_request("missing_required_fields")

        user = users_model.find_user_by_id(user_id)
        if user is None:
            return unauthorized("invalid_token")

        post = posts_model.create_post(
            title=title,
            content=content,
            author_id=user_id,
            author_nickname=user["nickname"],
            image_url=image_url,
        )
        return created("create_post_success", {"post_id": post["id"]})

    except Exception:
        return server_error()


def update_post(authorization: str | None, post_id: int, payload: dict) -> JSONResponse:
    try:
        user_id = _require_user_id(authorization)
        if user_id is None:
            return unauthorized("invalid_token")

        post = posts_model.find_post(post_id)
        if post is None:
            return not_found("post_not_found")

        if post["author_id"] != user_id:
            return forbidden("permission_denied")

        title = payload.get("title")
        content = payload.get("content")
        image_url = payload.get("image_url")

        if title is None and content is None and image_url is None:
            return bad_request("no_fields_to_update")

        posts_model.update_post(post_id, title=title, content=content, image_url=image_url)
        return ok("update_post_success", None)

    except Exception:
        return server_error()


def delete_post(authorization: str | None, post_id: int) -> JSONResponse:
    try:
        user_id = _require_user_id(authorization)
        if user_id is None:
            return unauthorized("invalid_token")

        post = posts_model.find_post(post_id)
        if post is None:
            return not_found("post_not_found")

        if post["author_id"] != user_id:
            return forbidden("permission_denied")

        posts_model.delete_post(post_id)
        return ok("delete_post_success", None)

    except Exception:
        return server_error()
