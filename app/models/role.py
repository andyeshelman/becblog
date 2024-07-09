from sqlalchemy.orm import Mapped, mapped_column

from typing import List

from app.modules import db

user_role = db.Table(
    'user_role',
    db.Model.metadata,
    db.Column('user', db.ForeignKey('user.id'), primary_key=True),
    db.Column('role', db.ForeignKey('role.id'), primary_key=True),
)

class Role(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(31))
    users: Mapped[List['User']] = db.relationship(secondary=user_role, back_populates='roles')