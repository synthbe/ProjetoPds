from uuid import UUID
from sqlalchemy.orm import joinedload

from app.models import Post, Audio, Comment
from app.schemas import PostCreate, PostUpdate

from .repository import Repository


class PostRepository(Repository[Post, PostCreate, PostUpdate]):
    @property
    def model(self) -> type[Post]:
        return Post

    def find_by_id(self, id: int | UUID) -> Post | None:
        return (
            self.db.query(Post)
            .options(
                joinedload(Post.audios),
                joinedload(Post.author),
                joinedload(Post.comments).joinedload(Comment.author),
            )
            .filter(Post.id == id)
            .first()
        )

    def create(self, data: PostCreate) -> Post:
        data_dict = data.model_dump()
        audio_ids = data_dict.pop("audio_ids", [])

        post = self.model(**data_dict)

        if audio_ids:
            audios = self.db.query(Audio).filter(Audio.id.in_(audio_ids)).all()
            post.audios.extend(audios)

        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_all(
        self, author_ids: list[UUID] | None = None, theme: str | None = None
    ) -> list[Post]:
        query = self.db.query(Post)

        if author_ids:
            query = query.filter(Post.author_id.in_(author_ids))

        if theme:
            query = query.filter(Post.theme.ilike(f"%{theme}%"))

        posts = (
            query.order_by(Post.created_at.desc())
            .options(
                joinedload(Post.audios),
                joinedload(Post.author),
                joinedload(Post.comments).joinedload(Comment.author),
            )
            .all()
        )

        for post in posts:
            post.comments.sort(key=lambda c: c.created_at)

        return posts

    def update(self, data: PostUpdate, model: Post) -> Post:
        data_dict = data.model_dump(exclude_unset=True)

        for key, value in data_dict.items():
            if key != "audio_ids":
                setattr(model, key, value)

        if "audio_ids" in data_dict:
            audio_ids = data_dict["audio_ids"] or []
            audios = self.db.query(Audio).filter(Audio.id.in_(audio_ids)).all()
            model.audios = audios

        self.db.commit()
        self.db.refresh(model)
        return model
