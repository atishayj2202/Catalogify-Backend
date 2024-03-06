from uuid import UUID

from fastapi import HTTPException
from firebase_admin import auth
from firebase_admin.auth import UserRecord
from starlette import status

from src.client.cockroach import CockroachDBClient
from src.client.computer_vision import ComputerVisionCli
from src.client.firebase import FirebaseClient
from src.client.openai_client import OpenAIClient
from src.db.table.feedback import Feedback
from src.db.table.post import Post
from src.db.table.user import User
from src.schemas.post import PostCreateRequest, PostLongResponse
from src.schemas.user import (
    RatingRequest,
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
)
from src.services.post import PostService


class UserService:
    @classmethod
    def fetch_user(cls, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
        )

    @classmethod
    def create_user(
        cls,
        request: UserCreateRequest,
        cockroach_client: CockroachDBClient,
        firebase_client: FirebaseClient,
    ) -> None:
        user: User = User(
            email=request.email,
            name=request.name,
            firebase_user_id=request.firebase_user_id,
        )
        user_firebase: UserRecord = auth.get_user(
            request.firebase_user_id, app=firebase_client.app
        )
        if (
            user_firebase.custom_claims is not None
            and firebase_client.user_key in user_firebase.custom_claims
        ):
            user.id = user_firebase.custom_claims[firebase_client.user_key]
        else:
            auth.set_custom_user_claims(
                request.firebase_user_id,
                {firebase_client.user_key: str(user.id)},
                app=firebase_client.app,
            )
        try:
            cockroach_client.query(
                User.add,
                items=[user],
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already found"
            )

    @classmethod
    def update_user(
        cls, user: User, request: UserUpdateRequest, cockroach_client: CockroachDBClient
    ):
        if request.email is not None and request.email != user.email:
            temp = cockroach_client.query(
                User.get_by_field_unique,
                field="email",
                match_value=request.email,
                error_not_exist=False,
            )
            if temp is not None and temp.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
                )
            user.email = request.email
        if request.name is not None and request.name != user.name:
            user.name = request.name
        cockroach_client.query(
            User.update_by_id,
            id=user.id,
            new_data=user,
        )

    @classmethod
    def add_feedback(
        cls, user: User, request: RatingRequest, cockroach_client: CockroachDBClient
    ) -> None:
        cockroach_client.query(
            Feedback.add,
            items=[
                Feedback(
                    from_user_id=user.id, rating=request.rate, feedback=request.comment
                )
            ],
        )

    @classmethod
    def fetch_user_by_id(
        cls, user_id: UUID, cockroach_client: CockroachDBClient
    ) -> UserResponse:
        user: User | None = cockroach_client.query(
            User.get_id, id=user_id, error_not_exist=False
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return cls.fetch_user(user)

    @classmethod
    def create_post(
        cls, user: User, request: PostCreateRequest, cockroach_client: CockroachDBClient,
        ai_client: OpenAIClient,
        image_parser_client: ComputerVisionCli
    ):
        post = Post(
            user_id=user.id,
            title=request.title,
            category=request.category,
            images=request.images,
            description=request.description,
            cost=request.cost,
            brand=request.brand,
            warranty_yrs=(request.warranty_months // 12),
            warranty_months=(request.warranty_months % 12),
            return_days=request.return_days,
            seller_location=request.seller_location,
            in_box=request.in_box,
        )
        cockroach_client.query(
            Post.add,
            items=[
                post
            ],
        )
        PostService.post_assessment(
            post=post,
            cockroach_client=cockroach_client,
            ai_client=ai_client,
            image_parser_client=image_parser_client,
        )

    @classmethod
    def fetch_posts(
        cls, user: User, cockroach_client: CockroachDBClient
    ) -> list[PostLongResponse]:
        posts: list[Post] | None = cockroach_client.query(
            Post.get_by_multiple_field_multiple,
            fields=["user_id", "is_deleted"],
            match_values=[user.id, None],
            error_not_exist=False,
        )
        if posts is None:
            return []
        temp: list[PostLongResponse] = []
        for post in posts:
            temp.append(
                PostLongResponse(
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
            )
        return temp
