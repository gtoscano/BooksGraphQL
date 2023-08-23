from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String as SQLString
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ariadne import make_executable_schema, gql, QueryType, MutationType
from ariadne.asgi import GraphQL

app = FastAPI()

DATABASE_URL = "postgresql://username:yourpassword@localhost/bookstore"

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(SQLString)
    author = Column(SQLString)
    year = Column(Integer)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# GraphQL SDL
type_defs = gql("""
type Book {
    id: Int!
    title: String!
    author: String!
    year: Int!
}

input BookInput {
    title: String!
    author: String!
    year: Int!
}

type Query {
    books: [Book!]!
    book(id: Int!): Book
}

type Mutation {
    createBook(bookData: BookInput!): Book!
    updateBook(id: Int!, bookData: BookInput!): Book!
    deleteBook(id: Int!): Int!
}
""")

# Resolvers
query = QueryType()
mutation = MutationType()

@query.field("books")
def resolve_books(*_):
    session = SessionLocal()
    try:
        books = session.query(Book).all()
        return books
    finally:
        session.close()

@query.field("book")
def resolve_book(*_, id):
    session = SessionLocal()
    try:
        book = session.query(Book).filter(Book.id == id).first()
        return book
    finally:
        session.close()

@mutation.field("createBook")
def resolve_create_book(*_, bookData):
    session = SessionLocal()
    try:
        new_book = Book(**bookData)
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        return new_book
    finally:
        session.close()

@mutation.field("updateBook")
def resolve_update_book(*_, id, bookData):
    session = SessionLocal()
    try:
        book = session.query(Book).filter(Book.id == id).first()
        for key, value in bookData.items():
            setattr(book, key, value)
        session.commit()
        # Fetch the book attributes before closing the session
        book_data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year
        }
    finally:
        session.close()

    return book_data
@mutation.field("updateBook")
def resolve_update_book(*_, id, bookData):
    session = SessionLocal()
    try:
        book = session.query(Book).filter(Book.id == id).first()
        for key, value in bookData.items():
            setattr(book, key, value)
        session.commit()
        
        # Fetch the book attributes before closing the session
        book_data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year
        }
    finally:
        session.close()
    
    return book_data


@mutation.field("deleteBook")
def resolve_delete_book(*_, id):
    session = SessionLocal()
    try:
        book = session.query(Book).filter(Book.id == id).first()
        session.delete(book)
        session.commit()
        return 1
    finally:
        session.close()

# Create executable schema
schema = make_executable_schema(type_defs, query, mutation)

# Add GraphQL route to FastAPI app
app.mount("/graphql", GraphQL(schema=schema))

