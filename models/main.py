from flask import Flask, jsonify, request
from book import Book
app = Flask(__name__)
import pyodbc

server = 'localhost'
database = 'TDD_Yannis'
username = 'sa'
password = 'Sql2019'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

cursor = conn.cursor()
cursor.execute("SELECT * FROM Book")
books = cursor.fetchall()

class Main:

    def __init__(self):
        self.books = []
        self.books.extend(iter(books))
        self.members = []
        self.reservations = []

    @app.route('/books', methods=['GET'])
    def get_all_books():
        book_list = []
        for book in books:
            book_obj = Book(book.isbn, book.title, book.author, book.editor, book.format, book.is_available)
            book_list.append(book_obj.__dict__)
        return jsonify(book_list)

    if __name__ == '__main__':
        app.run()
    
    def add_book(self, book):
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
