from uuid import UUID
from fastapi import Depends, Path, Query

from app.dependencies import AuthGuard
from app.models import User
from app.schemas.post_schema import PostCreateRequest, PostUpdate, PostResponse
from app.services.post_service import PostService

from .controller import BaseController


class PostController(BaseController):
    def __init__(self):
        super().__init__(tags=["Post"], prefix="/posts")
        self.post_service = PostService()

    def add_routes(self) -> None:
        @self.router.post("/", response_model=dict)
        def create_post(
            data: PostCreateRequest,
            user: User = Depends(AuthGuard.get_authenticated_user),
        ):
            return self.post_service.create_post(data, user)

        @self.router.get("/", response_model=list[PostResponse])
        def list_posts(theme: str | None = Query(default=None)):
            posts = self.post_service.get_all_posts()

            if theme:
                posts = [p for p in posts if p.theme == theme]

            return posts

        @self.router.get("/{post_id}", response_model=PostResponse)
        def get_post(post_id: UUID = Path(...)):
            post = self.post_service.get_post_by_id(post_id)
            return PostResponse.model_validate(post)

        @self.router.put("/{post_id}", response_model=PostResponse)
        def update_post(post_id: UUID, data: PostUpdate):
            updated_post = self.post_service.update_post(post_id, data)

            return PostResponse.model_validate(updated_post)

        @self.router.delete("/{post_id}", response_model=dict)
        def delete_post(post_id: UUID):
            return self.post_service.delete_post(post_id)
