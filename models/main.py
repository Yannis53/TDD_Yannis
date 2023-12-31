from flask import Flask, jsonify, request
from book import Book
from isbn_validator import ISBNValidator
from reservation import Reservation
import pyodbc
import datetime

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
    
    def search_books_by_title(self, title):
        return [book for book in self.books if book.title.lower() == title.lower()]
    
    def search_books_by_author(self, author):
        return [book for book in self.books if book.author.lower() == author.lower()]

    def search_books_by_isbn(self, isbn):
        return next((book for book in self.books if book.isbn == isbn), None)
    
    def add_member(self, member):
        self.members.append(member)
 
    def get_open_reservations(self, member=None):
        if member:
            return [reservation for reservation in self.reservations if reservation.member_id == member.id]
        else:
            return self.reservations
    
    def make_reservation(self, member, book):
        if len(self.get_open_reservations(member)) >= 3:
            raise Exception("Ce membre ne peut pas effectuer plus de réservations")
        limit_date = datetime.date.today() + datetime.timedelta(days=120)
        reservation_id = len(self.reservations) + 1
        reservation = Reservation(reservation_id, member.id, limit_date, book.isbn)
        self.reservations.append(reservation)
        return reservation
