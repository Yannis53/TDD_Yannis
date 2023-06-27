from flask import Flask, jsonify, request
from book import Book
from isbn_validator import ISBNValidator
import pyodbc

server = ''
database = ''
username = ''
password = ''
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

class Database:
    def __init__(self, conn):
        self.conn = conn

    def get_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Book")
        books = cursor.fetchall()
        book_list = []
        for book in books:
            isbn, title, author, editor, book_format, is_available = book
            book_obj = Book(isbn, title, author, editor, book_format, is_available)
            book_list.append(book_obj.__dict__)
        return book_list

app = Flask(__name__)
db = Database(conn)

class Main:

    def __init__(self):
        self.books = []
        self.members = []
        self.reservations = []

    # Route pour récupérer tous les livres
    @app.route('/books', methods=['GET'])
    def get_all_books(self):
        db = Database(self.conn)
        book_list = db.get_all_books()
        return jsonify(book_list)
    if __name__ == '__main__':
        app.run()
    
    def add_book(self, book):
        validator = ISBNValidator()
        if validator.validateISBN(book.isbn): # Vérifie que l'isbn du livre est conforme
            self.books.append(book)
    
    def update_book(self, book):
        for i, b in enumerate(self.books):
            if b.isbn == book.isbn:
                self.books[i].title = book.title
                self.books[i].author = book.author
                self.books[i].editor = book.editor
                self.books[i].format = book.format
                self.books[i].is_available = book.is_available
                break

    def remove_book(self, book):
        self.books = [b for b in self.books if b != book]
