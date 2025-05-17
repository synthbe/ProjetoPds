from uuid import UUID

from fastapi.responses import JSONResponse
from fastapi import status

from app.repositories import PostRepository, AudioRepository
from app.schemas.post_schema import PostCreateRequest, PostCreate, PostUpdate
from app.exceptions import NotFoundException
from app.models import User


class PostService:
    def __init__(self):
        self.post_repository = PostRepository()
        self.audio_repository = AudioRepository()

    def create_post(self, data: PostCreateRequest, user: User) -> JSONResponse:
        audio_ids = data.audio_ids
        audios = self.audio_repository.get_by_ids(audio_ids)
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
