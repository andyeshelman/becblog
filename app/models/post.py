from app.modules.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    body: Mapped[str] = mapped_column(db.String(15000))
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[List['Comment']] = relationship(back_populates='post', cascade='all')