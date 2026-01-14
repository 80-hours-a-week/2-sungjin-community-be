from __future__ import annotations

from typing import TypedDict, NotRequired


class Post(TypedDict):
    id: int
    title: str
    content: str
    author_id: int
    author_nickname: str
    image_url: NotRequired[str]


_POSTS: list[Post] = [
    {
        "id": 1,
        "title": "welcome",
        "content": "Welcome to Community!",
        "author_id": 1,
        "author_nickname": "starter",
    },
    {
        "id": 2,
        "title": "rules",
        "content": "Be kind and respectful.",
        "author_id": 999,
        "author_nickname": "admin",
    },
]

_next_id: int = 3


def list_posts(page: int = 1, limit: int = 10) -> list[Post]:
    start = (page - 1) * limit
    end = start + limit
    return _POSTS[start:end]


def find_post(post_id: int) -> Post | None:
    return next((p for p in _POSTS if p["id"] == post_id), None)


def create_post(title: str, content: str, author_id: int, author_nickname: str, image_url: str | None = None) -> Post:
    global _next_id
    post: Post = {
        "id": _next_id,
        "title": title,
        "content": content,
        "author_id": author_id,
        "author_nickname": author_nickname,
    }
    if image_url:
        post["image_url"] = image_url
    _POSTS.append(post)
    _next_id += 1
    return post


def update_post(post_id: int, title: str | None = None, content: str | None = None, image_url: str | None = None) -> Post | None:
    post = find_post(post_id)
    if post is None:
        return None
    if title is not None:
        post["title"] = title
    if content is not None:
        post["content"] = content
    if image_url is not None:
        post["image_url"] = image_url
    return post


def delete_post(post_id: int) -> bool:
    idx = next((i for i, p in enumerate(_POSTS) if p["id"] == post_id), None)
    if idx is None:
        return False
    _POSTS.pop(idx)
    return True
