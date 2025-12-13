# MyBookShelf


MyBookShelf is a web application for managing books, authors, and user booklists. 
Users can browse books and authors, add their own suggested changes, manage favorite authors, 
and create their own booklists. Administrators can approve or reject suggested changes to books.

## Functionality

- Storing books in the database
- Searching for books by title, author name, or genre
- Creating custom book lists (available to authenticated users only)
- Adding books to book lists (available to authenticated users only)
- User registration and login
- Protection of private book lists using authentication
- Administrative interface for data management
- Automated tests using **pytest**

## Database model

### Models
- **Author**
- **Book**
- **BookList**
- **BookListItem**
- **UserProfile**
- **Genre**

### Relationships

- **Author ↔ Book** (**M:N**)  
  A book can have multiple authors, and an author can write multiple books.

- **Book ↔ Genre** (**M:N**)  
  A book can belong to multiple genres, and a genre can include multiple books.

- **Book ↔ BookList** (**M:N** via `BookListItem`)  
  The relationship is implemented using a bridging model that also stores the date when a book was added to a list.

- **User ↔ BookList** (**1:N**)  
  A user can own multiple book lists, while each book list belongs to exactly one user.

- **User ↔ UserProfile** (**1:1**)  
  Each user has a single extended profile containing reading preferences.

- **UserProfile ↔ Genre** (**M:N**)  
  A user can have multiple favorite genres, and a genre can be favorited by multiple users.

- **UserProfile ↔ Author** (**M:N**)  
  A user can follow multiple authors, and an author can be followed by multiple users.

- **User ↔ Book (created_by)** (**1:N**, optional)  
  A user can create multiple book records, while a book may also be created by the system.

---

## Technologies

- Python 3.x
- Django
- PostgreSQL
- Django ORM
- HTML / CSS
- pytest

---

## Installation

1. Clone the repository:

git clone https://github.com/JolanaB169/MyBookShelf.git
cd MyBookShelf

2. Create and activate a virtual environment::

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Apply database migrations:

python manage.py makemigrations
python manage.py migrate

5. Run the development server:

python manage.py runserver

The project should now be running at: http://127.0.0.1:8000/

---
