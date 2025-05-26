from uuid import UUID

from fastapi.responses import JSONResponse
from fastapi import status

from app.repositories import PostRepository, AudioRepository, CommentRepository
from app.schemas import PostCreateRequest, PostCreate, PostUpdate, CommentCreate
from app.exceptions import NotFoundException
from app.models import User


class PostService:
    def __init__(self):
        self.post_repository = PostRepository()
        self.audio_repository = AudioRepository()
        self.comment_repository = CommentRepository()

    def create_post(self, data: PostCreateRequest, user: User) -> JSONResponse:
        audio_ids = data.audio_ids
        audios = self.audio_repository.find_by_ids(audio_ids)
        audios_dict = {audio.id: audio for audio in audios}

        missing_audio_ids = []

        for audio_id in audio_ids:
            audio = audios_dict.get(audio_id)

            if not audio or audio.user_id != user.id:
                missing_audio_ids.append(audio_id)

        if missing_audio_ids:
            missing_audio_id_str = ", ".join(str(id) for id in missing_audio_ids)
            raise NotFoundException(
                "Audio files not found",
                errors=[f"Audio files with IDs: {missing_audio_id_str} not found"],
            )

        post = self.post_repository.create(
            PostCreate(**data.model_dump(), author_id=user.id)
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"id": str(post.id), "message": "Post created successfully"},
        )

    def get_post_by_id(self, post_id: UUID):
        post = self.post_repository.find_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found")

        return post

    def get_my_posts(self, user: User, theme: str | None = None):
        return self.post_repository.get_all(author_ids=[user.id], theme=theme)

    def get_feed_posts(self, user: User, theme: str | None = None):
        following_ids = [u.id for u in user.following]
        author_ids = [user.id] + following_ids
        return self.post_repository.get_all(theme=theme, author_ids=author_ids)

    def delete_post(self, post_id: UUID) -> JSONResponse:
        post = self.post_repository.find_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found")

        self.post_repository.delete(post)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Post deleted successfully"},
        )

    def update_post(self, post_id: UUID, data: PostUpdate):
        post = self.post_repository.find_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found")

        updated_post = self.post_repository.update(data, post)

        return updated_post

    def add_comment(
        self, post_id: UUID, data: CommentCreate, user: User
    ) -> JSONResponse:
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise NotFoundException("Post not found")

        self.comment_repository.create(
            CommentCreate(
                content=data.content,
                post_id=post_id,
                author_id=user.id,
            )
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Comment added successfully"},
        )
