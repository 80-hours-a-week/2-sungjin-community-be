from __future__ import annotations

from fastapi import APIRouter, Header, Query
from app.controllers import posts_controller

router = APIRouter()

@router.get("")
def list_posts(
    authorization: str | None = Header(default=None),
    page: int = Query(default=1),
    limit: int = Query(default=10),
):
    return posts_controller.list_posts(authorization, page=page, limit=limit)


@router.get("/{post_id}")
def get_post_detail(
    post_id: int,
    authorization: str | None = Header(default=None),
):
    return posts_controller.get_post_detail(authorization, post_id)


@router.post("")
def create_post(
    payload: dict,
    authorization: str | None = Header(default=None),
):
    return posts_controller.create_post(authorization, payload)


@router.put("/{post_id}")
def update_post(
    post_id: int,
    payload: dict,
    authorization: str | None = Header(default=None),
):
    return posts_controller.update_post(authorization, post_id, payload)


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    authorization: str | None = Header(default=None),
):
    return posts_controller.delete_post(authorization, post_id)
