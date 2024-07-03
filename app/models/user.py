from app.database import db
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)