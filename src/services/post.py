from starlette import status
from starlette.exceptions import HTTPException

from src.client.cockroach import CockroachDBClient
from src.db.table.post import Post
from src.schemas.post import PostEditRequest, PostLongResponse
from src.utils.time import get_current_time


class PostService:
    @classmethod
    def fetch_post(cls, post: Post) -> PostLongResponse:
        return PostLongResponse(
            id=post.id,
            created_at=post.created_at,
            user_id=post.user_id,
            title=post.title,
            category=post.category,
            images=post.images,
            description=post.description,
            cost=post.cost,
            brand=post.brand,
            warranty_yrs=post.warranty_yrs,
            warranty_months=post.warranty_months,
            return_days=post.return_days,
            seller_location=post.seller_location,
            in_box=post.in_box,
        )

    @classmethod
    def edit_post(
        cls, post: Post, request: PostEditRequest, cockroach_client: CockroachDBClient
    ):
        if request.title is not None:
            post.title = request.title
        if request.images is not None:
            post.images = request.images
        if request.description is not None:
            post.description = request.description
        if request.cost is not None:
            post.cost = request.cost
        if request.brand is not None:
            post.brand = request.brand
        if request.seller_location is not None:
            post.seller_location = request.seller_location
        if request.in_box is not None:
            post.in_box = request.in_box
        cockroach_client.query(Post.update_by_id, id=post.id, new_data=post)

    @classmethod
    def delete_post(cls, post: Post, cockroach_client: CockroachDBClient):
        if post.is_deleted is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Post already deleted"
            )
        post.is_deleted = get_current_time()
        cockroach_client.query(Post.update_by_id, id=post.id, new_data=post)
