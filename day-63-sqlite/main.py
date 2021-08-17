import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float(), nullable=False)

    # def __repr__(self):
    #     return f"{self.title}"

###### create the database
db.create_all()

###### reads all records
all_books = Books.query.all()
print(all_books)
print(len(all_books))

###### partial read by filter
# book = Books.query.filter_by(title="Good Book 3").first()
# print(book)

###### partial read by PRIMARY KEY
book_id = 1
book = Books.query.get(book_id)
print(book)
print(book.title, book.author, book.rating)

###### partial update
# book_to_update = Books.query.filter_by(title="Good Book 3").first()
# book_to_update.title = "Good Book 3 Revision 2"
# db.session.commit()

###### re-read the updated data
# book = Books.query.filter_by(title="Good Book 3 Revision 2").first()
# print(book)

# ###### update data by id (PRIMARY KEY)
# book_id = 1
# book_to_update = Books.query.get(book_id)
# print(book_to_update)
# book_to_update.title = "Good Book Revision 2"
# db.session.commit()
#
# ###### re-read the updated data
# book = Books.query.get(book_id)
# print(book)
#

# ###### delete a particular record by PRIMARY KEY
# book_id = 2
# book_to_delete = Books.query.get(book_id)
# print(book_to_delete)
# db.session.delete(book_to_delete)
# db.session.commit()

# ###### read all records after update
# all_books = Books.query.all()
# print(all_books)

# add a records of data
# new_book = Books(title="Good Book", author="Good Author", rating="8")
# new_book2 = Books(title="Good Book 2", author="Good Author 2", rating="9")
# new_book3 = Books(title="Good Book 3", author="Good Author 3", rating="10")
#
# db.session.add(new_book)
# db.session.add(new_book2)
# db.session.add(new_book3)
# db.session.commit()

###### SQLITE3 SESSION
# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()

# cursor.execute("CREATE TABLE books(id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE,"
#                " author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

# cursor.execute("INSERT INTO books VALUES(1, 'Good Book', 'Good Author', '8')")
# db.commit()
