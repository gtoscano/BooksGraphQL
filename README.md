# BooksGraphQL

BooksGraphQL is a simple example demonstrating how to use FastAPI with GraphQL. This project provides a GraphQL API for managing books in a straightforward manner, making it suitable for those who are new to integrating GraphQL with FastAPI.

## Setup

### Database Setup

Before running the application, you need to set up a PostgreSQL database:

1. **Install PostgreSQL**:
   If you haven't installed PostgreSQL, you can download it from [here](https://www.postgresql.org/download/).

2. **Create a new database**:

```bash
createdb bookstore
```

3. **Set up a user and grant permissions**:

First, enter the PostgreSQL interactive terminal:

```bash
psql -U your_superuser_name -h localhost -d bookstore
```

Replace `your_superuser_name` with your PostgreSQL superuser name. 

Then, create a user and grant necessary permissions:

```sql
CREATE USER username WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE bookstore TO username;
GRANT USAGE, SELECT ON SEQUENCE books_id_seq TO username;
```

Replace `username` with your desired username and `yourpassword` with your desired password.

4. **Update the `DATABASE_URL`**:
   Ensure the `DATABASE_URL` in the code matches your PostgreSQL credentials and database.

### Application Setup

1. **Clone the repository**:

```bash
git clone https://github.com/YOUR_USERNAME/BooksGraphQL.git
cd BooksGraphQL
```

2. **Install the required dependencies**:

```bash
pipenv install
```

3. **Run the FastAPI application**:

```bash
pipenv run uvicorn main:app --reload
```

This will start the server on `http://127.0.0.1:8000/`.

## Accessing GraphQL Playground

Once the server is running, you can access the GraphQL Playground by navigating to `http://127.0.0.1:8000/graphql`.

Here are some example queries and mutations you can try:

### Queries

1. Fetch all books:

```graphql
{
  books {
    id
    title
    author
    year
  }
}
```

2. Fetch a specific book by ID:

```graphql
{
  book(id: 1) {
    id
    title
    author
    year
  }
}
```

### Mutations

1. Create a new book:

```graphql
mutation {
  createBook(bookData: {title: "Dune", author: "Frank Herbert", year: 1965}) {
    id
    title
    author
    year
  }
}
```

2. Update a book's details:

```graphql
mutation {
  updateBook(id: 1, bookData: {title: "Dune Messiah", author: "Frank Herbert", year: 1969}) {
    id
    title
    author
    year
  }
}
```

3. Delete a book by ID:

```graphql
mutation {
  deleteBook(id: 1)
}
```

This will return `1` if the deletion was successful.



## License

This project is licensed under the Apache License 2.0. For detailed information, refer to the [LICENSE](LICENSE) file in the repository. The Apache License 2.0 is a permissive license that allows for the freedom to use the software for any purpose, to distribute it, to modify it, and to distribute modified versions of the software, under the terms of the license.
