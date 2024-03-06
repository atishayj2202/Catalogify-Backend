from starlette import status
from starlette.exceptions import HTTPException

from src.client.cockroach import CockroachDBClient
from src.client.computer_vision import ComputerVisionCli
from src.client.openai_client import OpenAIClient
from src.db.table.assessment import Assessment
from src.db.table.post import Post
from src.schemas.post import AssessmentResponse, PostEditRequest, PostLongResponse
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

    @classmethod
    def post_assessment(
        cls,
        post: Post,
        cockroach_client: CockroachDBClient,
        ai_client: OpenAIClient,
        image_parser_client: ComputerVisionCli,
    ):
        temp = []
        for i in post.images:
            temp.append(image_parser_client.analyze_image(i))
        assess = ai_client.get_assessment_reply(
            title=post.title, images=temp, description=post.description
        )
        score = (
            int(not assess["assessment 5"])
            + int(not assess["assessment 4"])
            + int(not assess["assessment 3"])
            + int(not assess["assessment 1"])
        ) * 10
        score = score + (len(assess["assessment 2"]) * 5)
        score = 100 - score
        temp2: Assessment | None = cockroach_client.query(
            Assessment.get_by_field_unique,
            field="post_id",
            match_value=post.id,
            error_not_exist=False,
        )
        if temp2 is not None:
            cockroach_client.query(Assessment.delete_by_id, id=temp2.id)
        cockroach_client.query(
            Assessment.add,
            items=[
                Assessment(
                    post_id=post.id,
                    assessment1=assess["assessment 1"],
                    assessment2=[str(integer) for integer in assess["assessment 2"]],
                    assessment3=assess["assessment 3"],
                    assessment4=assess["assessment 4"],
                    assessment5=assess["assessment 5"],
                    assessment6=assess["assessment 6"],
                    total=score,
                )
            ],
        )

    @classmethod
    def fetch_assessment(
        cls, post: Post, cockroach_client: CockroachDBClient
    ) -> AssessmentResponse:
        assess: Assessment | None = cockroach_client.query(
            Assessment.get_by_field_unique,
            field="post_id",
            match_value=post.id,
            error_not_exist=False,
        )
        if assess is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Post Not Found"
            )
        return AssessmentResponse(
            post_id=assess.post_id,
            assessment1=assess.assessment1,
            assessment2=assess.assessment2,
            assessment3=assess.assessment3,
            assessment4=assess.assessment4,
            assessment5=assess.assessment5,
            recommendation=assess.assessment6,
            total=assess.total,
        )
