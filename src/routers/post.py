from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.auth.user_auth import VerifiedPost, verify_post
from src.client.cockroach import CockroachDBClient
from src.schemas.post import PostEditRequest, PostLongResponse
from src.services.post import PostService
from src.utils.client import getCockroachClient

POST_PREFIX = "/post"
post_router = APIRouter(prefix=POST_PREFIX)
ENDPOINT_GET_POST = "/{post_id}/get-post/"  # done
ENDPOINT_EDIT_POST = "/{post_id}/edit-post/"  # done
ENDPOINT_DELETE_POST = "/{post_id}/delete-post/"  # pending
ENDPOINT_GET_ASSESSMENT = "/{post_id}/get-assessment/"  # pending
ENDPOINT_GET_CATALOG = "/{post_id}/get-catalog/"  # pending
ENDPOINT_GET_COMPETITORS = "/{post_id}/get-competitors/"  # pending


@post_router.get(ENDPOINT_GET_POST, response_model=PostLongResponse)
async def get_post(
    verified_post: VerifiedPost = Depends(verify_post),
):
    return PostService.fetch_post(post=verified_post.requesting_post)


@post_router.post(ENDPOINT_EDIT_POST)
async def post_edit_post(
    request: PostEditRequest,
    verified_post: VerifiedPost = Depends(verify_post),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    PostService.edit_post(
        post=verified_post.requesting_post,
        request=request,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)


@post_router.post(ENDPOINT_DELETE_POST)
async def get_delete_post(
    verified_post: VerifiedPost = Depends(verify_post),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    PostService.delete_post(
        post=verified_post.requesting_post, cockroach_client=cockroach_client
    )
    return Response(status_code=status.HTTP_200_OK)
