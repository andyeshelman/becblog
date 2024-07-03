from app.database import db
from sqlalchemy.orm import Mapped, mapped_column

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    body: Mapped[str] = mapped_column(db.Text)
    user_id: Mapped[int] = mapped_column(db.Integer, nullable=False)