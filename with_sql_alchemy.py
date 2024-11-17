from __future__ import annotations

from sqlalchemy import ForeignKey, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

# 데이터베이스 연결
"""Valid SQLite URL forms are:
 sqlite:///:memory: (or, sqlite://)
 sqlite:///relative/path/to/file.db
 sqlite:////absolute/path/to/file.db
 """
engine = create_engine("sqlite:///blog.db", echo=True)  # echo키면 로그나옴


# 베이스 클래스 정의
class Base(DeclarativeBase):
    pass


# 유저 테이블 정의
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[list[Post]] = relationship(back_populates="user")


# 포스트 테이블 정의
class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[User] = relationship(back_populates="posts")


# 테이블 생성
Base.metadata.create_all(engine)

# 세션 생성

with Session(engine) as session:
    # 데이터 삽입
    user1 = User(username="user1", email="user1@example.com")
    user2 = User(username="user2", email="user2@example.com")
    session.add(user1)
    session.add(user2)
    session.commit()

    post1 = Post(user_id=user1.id, title="First Post", content="This is the first post")
    post2 = Post(
        user_id=user2.id, title="Second Post", content="This is the second post"
    )
    session.add_all([post1, post2])
    session.commit()

    # 조인 쿼리 -> .query 쓰는게 레거시긴 함. 1.0문법이고, 2.0부터는 select() 써야함.
    results = session.query(User.username, Post.title, Post.content).join(Post).all()
    for username, title, content in results:
        print(f"Username: {username}, Title: {title}, Content: {content}")

    # 조건부 검색문
    stmt = select(Post).where(Post.title.in_(["First Post", "Second Post"]))
    for post in session.scalars(stmt):
        print(f"Title: {post.title}, Content: {post.content}")

    # 데이터 업데이트
    user1.email = "newemail@example.com"
    session.commit()

    # 업데이트된 데이터 확인
    updated_users = session.scalars(select(User))
    for user in updated_users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
