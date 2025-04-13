from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    # Propiedades adicionales de perfil
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120))
    bio: Mapped[str] = mapped_column(Text(), default="")
    profile_image: Mapped[str] = mapped_column(String(250))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relaciones con otros modelos
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    # Relaciones de seguimiento (seguidores y seguidos)
    followers = relationship("Follow", foreign_keys="Follow.followed_id", back_populates="followed")
    following = relationship("Follow", foreign_keys="Follow.follower_id", back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "bio": self.bio,
            "profile_image": self.profile_image,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class Post(db.Model):
    __tablename__ = 'post'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    image_url: Mapped[str] = mapped_column(String(250), nullable=False)
    caption: Mapped[str] = mapped_column(Text())
    location: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relaciones
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "caption": self.caption,
            "location": self.location,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relaciones
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class Like(db.Model):
    __tablename__ = 'like'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relaciones
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class Follow(db.Model):
    __tablename__ = 'follow'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    followed_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relaciones: Un usuario (follower) sigue a otro usuario (followed)
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

if __name__ == "__main__":
    # Al ejecutar este archivo se generará el diagrama ER en 'diagram.png'
    # Se requiere instalar la librería ERAlchemy: pip install eralchemy
    from eralchemy import render_er
    render_er(db.metadata, 'diagram.png')
    print("Diagrama generado en diagram.png")
