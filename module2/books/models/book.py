from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from module2.database import Base


class Genre(Base):
    """ Название жанра """
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    name_genre = Column(String(255), unique=True, nullable=False)


class Author(Base):
    """ Автор книг """
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name_author = Column(String(255), nullable=False)


class Book(Base):
    """ Название книги, цена, количество на складе, id жанра и автора """
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Integer, default=0, nullable=False)
    genre_id = Column(Integer, ForeignKey("genre.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)

    genre = relationship("Genre", back_populates="books")
    author = relationship("Author", back_populates="books")


Genre.books = relationship("Book", back_populates="genre")
Author.books = relationship("Book", back_populates="author")
