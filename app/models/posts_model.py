from __future__ import annotations

from typing import Dict, List, Optional


# ===== In-memory storage =====
_posts: Dict[int, dict] = {}
_post_seq: int = 1


def create_post(user_id: int, title: str, content: str, image: Optional[str] = None) -> dict:
    """게시글 생성"""
    global _post_seq

    post = {
        "id": _post_seq,
        "user_id": user_id,
        "title": title,
        "content": content,
        "image": image,
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
    }
    _posts[_post_seq] = post
    _post_seq += 1
    return post


def list_posts(page: int = 1, limit: int = 10) -> dict:
    """게시글 목록 (페이지네이션)"""
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10

    items: List[dict] = sorted(_posts.values(), key=lambda x: x["id"], reverse=True)

    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    sliced = items[start:end]

    # 목록용으로 필요한 필드만 내려주는 형태(가벼움)
    results = [
        {
            "post_id": p["id"],
            "title": p["title"],
            "author_id": p["user_id"],
            "view_count": p["view_count"],
            "like_count": p["like_count"],
            "comment_count": p["comment_count"],
        }
        for p in sliced
    ]

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "posts": results,
    }


def find_post_by_id(post_id: int) -> Optional[dict]:
    return _posts.get(post_id)


def increase_view(post_id: int) -> None:
    post = _posts.get(post_id)
    if post:
        post["view_count"] += 1


def update_post(post_id: int, title: Optional[str] = None, content: Optional[str] = None, image: Optional[str] = None) -> Optional[dict]:
    post = _posts.get(post_id)
    if post is None:
        return None

    if title is not None:
        post["title"] = title
    if content is not None:
        post["content"] = content
    if image is not None:
        post["image"] = image

    return post


def delete_post(post_id: int) -> bool:
    return _posts.pop(post_id, None) is not None
