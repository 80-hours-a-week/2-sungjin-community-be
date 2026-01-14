
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class AppError:
    status_code: int
    message: str


INVALID_REQUEST = AppError(400, "invalid_request")
MISSING_FIELD = AppError(400, "missing_field")
INVALID_FIELD = AppError(400, "invalid_field")

EMAIL_ALREADY_EXISTS = AppError(409, "email_already_exists")
NICKNAME_ALREADY_EXISTS = AppError(409, "nickname_already_exists")

EMAIL_NOT_FOUND = AppError(400, "email_not_found")
PASSWORD_MISMATCH = AppError(400, "password_mismatch")

UNAUTHORIZED = AppError(401, "unauthorized")
FORBIDDEN = AppError(403, "permission_denied")

POST_NOT_FOUND = AppError(404, "post_not_found")
COMMENT_NOT_FOUND = AppError(404, "comment_not_found")
USER_NOT_FOUND = AppError(404, "user_not_found")

INTERNAL_SERVER_ERROR = AppError(500, "internal_server_error")
