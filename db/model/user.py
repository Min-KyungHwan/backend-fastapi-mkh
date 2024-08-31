from sqlalchemy import Integer, String, VARCHAR
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "Users"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_name = mapped_column(VARCHAR(256), nullable=False, unique=True)
    email = mapped_column(VARCHAR(256), nullable=False)
    password = mapped_column(VARCHAR(256), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} and username {self.user_name}"
