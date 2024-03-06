from uuid import UUID

from fastapi import Depends, Header, HTTPException
from pydantic import BaseModel
from starlette import status

from src.auth.base import _get_requesting_user
from src.client.cockroach import CockroachDBClient
from src.client.firebase import FirebaseClient
from src.db.table.post import Post
from src.db.table.user import User
from src.utils.client import getCockroachClient, getFirebaseClient


class VerifiedUser(BaseModel):
    requesting_user: User


class VerifiedPost(BaseModel):
    requesting_user: User
    requesting_post: Post


def verify_user(
    authorization: str = Header(...),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
    firebase_client: FirebaseClient = Depends(getFirebaseClient),
) -> VerifiedUser:
    user: User = _get_requesting_user(authorization, cockroach_client, firebase_client)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return VerifiedUser(requesting_user=user)


def verify_post(
    post_id: UUID,
    authorization: str = Header(...),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
    firebase_client: FirebaseClient = Depends(getFirebaseClient),
) -> VerifiedPost:
    user: User | None = _get_requesting_user(
        authorization, cockroach_client, firebase_client
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    post: Post | None = cockroach_client.query(
        Post.get_id,
        id=post_id,
        error_not_exist=False,
    )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized to access post",
        )
    return VerifiedPost(requesting_user=user, requesting_post=post)
