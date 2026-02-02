from fastapi.responses import JSONResponse
from app.common.responses import ok, created

from app.common.exceptions import (
    BusinessException, ErrorCode,
    MissingRequiredFieldsError, PostNotFoundError,
    CommentNotFoundError, ForbiddenError,
    InvalidRequestFormatError
)
from app.models import posts_model, comments_model


def _validate_comment(content: str) -> None:
    
    if len(content) > 500:
        raise BusinessException(
            ErrorCode.INVALID_REQUEST_FORMAT,
            "댓글은 최대 500자까지 가능합니다."
        )


def list_comments(post_id: int, user_id: int | None = None) -> JSONResponse:

    if not posts_model.find_post(post_id):
        raise PostNotFoundError()
    
    comments = comments_model.list_comments(post_id, user_id)
    return ok(message="read_comments_success", data=comments)


def create_comment(user_id: int, post_id: int, payload: dict) -> JSONResponse:
    content = (payload.get("content") or "").strip()
    
   
    if not content:
        raise MissingRequiredFieldsError("댓글 내용을 입력해주세요.")

    _validate_comment(content)

    if not posts_model.find_post(post_id):
        raise PostNotFoundError()

    comment = comments_model.create_comment(user_id, post_id, content)
    return created(message="comment_created", data=comment)



def update_comment(user_id: int, post_id: int, comment_id: int, payload: dict) -> JSONResponse:
    comment = comments_model.find_comment(comment_id)
    if not comment:
        raise CommentNotFoundError()

    
    if comment["post_id"] != post_id:
        raise CommentNotFoundError()

    # 권한 체크
    if comment["user_id"] != user_id:
        raise ForbiddenError("댓글 수정 권한이 없습니다.")

    content = (payload.get("content") or "").strip()
    
    if not content:
        raise MissingRequiredFieldsError("댓글 내용을 입력해주세요.")
        
    _validate_comment(content)


    updated = comments_model.update_comment(comment_id, content)
    if not updated:
        raise CommentNotFoundError()

    return ok(message="comment_updated", data=updated)


def delete_comment(user_id: int, post_id: int, comment_id: int) -> JSONResponse:
    comment = comments_model.find_comment(comment_id)
    if not comment:
        raise CommentNotFoundError()

   
    if comment["post_id"] != post_id:
        raise CommentNotFoundError()

   
    if comment["user_id"] != user_id:
        raise ForbiddenError("댓글 삭제 권한이 없습니다.")

    comments_model.delete_comment(comment_id)
    return ok(message="comment_deleted", data=None)