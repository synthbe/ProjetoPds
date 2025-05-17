from uuid import UUID

from fastapi.responses import JSONResponse
from fastapi import status

from app.repositories.post_repository import PostRepository
from app.schemas.post_schema import PostCreate, PostUpdate
from app.exceptions import NotFoundException


class PostService:
    def __init__(self):
        self.post_repository = PostRepository()

    def create_post(self, data: PostCreate) -> JSONResponse:
        post = self.post_repository.create(data)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"id": str(post.id), "message": "Post created successfully"},
        )

    def get_post_by_id(self, post_id: UUID):
        post = self.post_repository.get_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found")

        return post

    def get_all_posts(self):
        return self.post_repository.get_all()

    def delete_post(self, post_id: UUID) -> JSONResponse:
        post = self.post_repository.get_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found")

        self.post_repository.delete(post)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Post deleted successfully"},
        )

    def update_post(self, post_id: UUID, data: PostUpdate):
        post = self.post_repository.get_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found")

        updated_post = self.post_repository.update(data, post)

        return updated_post
