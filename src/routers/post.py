from fastapi import APIRouter

POST_PREFIX = "/post"
post_router = APIRouter(prefix=POST_PREFIX)
ENDPOINT_GET_POST = "/{post_id}/get-post/"  # pending
ENDPOINT_EDIT_POST = "/{post_id}/edit-post/"  # pending
ENDPOINT_GET_ASSESSMENT = "/{post_id}/get-assessment/"  # pending
ENDPOINT_GET_CATALOG = "/{post_id}/get-catalog/"  # pending
ENDPOINT_GET_COMPETITORS = "/{post_id}/get-competitors/"  # pending
