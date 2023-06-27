import unittest
from unittest.mock import patch
from unittest import mock
import datetime
from isbn_validator import ISBNValidator
from main import Main, app, Database
from book import Book
from member import Member

class Test(unittest.TestCase):


    def setUp(self):
        self.library = Main()
        self.book1 = Book("2210765528", "Livre test 1", "Auteur test 1", "Éditeur test 1", "Poche", True)
        self.book2 = Book("140274577X", "Livre test 2", "Auteur test 2", "Éditeur test 2", "BD", True)
        self.member = Member("Code1", "Yannis", "ZEMIRLINE", datetime.date(1993, 12, 15), "Homme")
        self.app = app.test_client()
        self.conn_mock = mock.Mock()
        self.db = Database(self.conn_mock)

    def test_add_book(self):
        self.library.add_book(self.book1)
        self.assertIn(self.book1, self.library.books)

    def test_update_book(self):
        self.library.add_book(self.book1)
        updated_book = Book("2210765528", "Livre test 1.2", "Auteur test 1.2", "Éditeur test 1.2", "Broché", False)
        self.library.update_book(updated_book)
        self.assertEqual(self.book1.title, "Livre test 1.2")
        self.assertEqual(self.book1.author, "Auteur test 1.2")
        self.assertEqual(self.book1.editor, "Éditeur test 1.2")
        self.assertEqual(self.book1.format, "Broché")
        self.assertFalse(self.book1.is_available)

    def test_remove_book(self):
        self.library.add_book(self.book1)
        self.library.remove_book(self.book1)
        self.assertNotIn(self.book1, self.library.books)

    def test_checkValid10CharsISBNCode(self):
        validator = ISBNValidator()
        result = validator.validateISBN("2210765528")
        self.assertTrue(result, "first assertion")
        result = validator.validateISBN("2226392122")
        self.assertTrue(result, "second assertion")
    
    def test_checkInvalid10CharsISBNCode(self):
        validator = ISBNValidator()
        result = validator.validateISBN("2210765525")
        self.assertFalse(result)

    def test_invalidLengthShouldThrowsException(self):
        validator = ISBNValidator()
        self.assertRaises(ValueError, validator.validateISBN, "123456789")
        self.assertRaises(ValueError, validator.validateISBN, "12345678912")

    def test_nonNumericISBNThrowsException(self):
        validator = ISBNValidator()
        self.assertRaises(ValueError, validator.validateISBN, "helloworld")

    def test_checkISBNEndingWithAnXIsValid(self):
        validator = ISBNValidator()
        result = validator.validateISBN("140274577X")
        self.assertTrue(result)

    def test_checkValid13CharsISBNCode(self):
        validator = ISBNValidator()
        result = validator.validateISBN("9781402745775")
        self.assertTrue(result)
    
    def test_get_all_books(self):

        # Création d'un mock du curseur de la base de données
        cursor_mock = mock.Mock()

        # Définition des valeurs de retour du curseur pour simuler les résultats de la requête SQL
        cursor_mock.fetchall.return_value = [
            ('1234567890', 'Book 1', 'Author 1', 'Editor 1', 'Format 1', True),
            ('0987654321', 'Book 2', 'Author 2', 'Editor 2', 'Format 2', False)
        ]

        # Configuration du mock de la connexion pour retourner le mock du curseur
        self.db.conn.cursor.return_value = cursor_mock

        # Appel de la méthode à tester en passant le mock de la connexion comme paramètre
        result = self.db.get_all_books()

        # Vérification que la méthode cursor() a été appelée sur la connexion
        self.db.conn.cursor.assert_called_once()

        # Vérification que la méthode execute() a été appelée sur le curseur avec la requête SQL appropriée
        cursor_mock.execute.assert_called_once_with("SELECT * FROM Book")

        # Vérification que la méthode fetchall() a été appelée sur le curseur
        cursor_mock.fetchall.assert_called_once()

        # Vérification des résultats
        expected_result = [
            {
                'isbn': '1234567890',
                'title': 'Book 1',
                'author': 'Author 1',
                'editor': 'Editor 1',
                'format': 'Format 1',
                'is_available': True
            },
            {
                'isbn': '0987654321',
                'title': 'Book 2',
                'author': 'Author 2',
                'editor': 'Editor 2',
                'format': 'Format 2',
                'is_available': False
            }
        ]
        self.assertEqual(result, expected_result)
    
    def test_search_books_by_title(self):
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        result = self.library.search_books_by_title("Livre test 2")
        self.assertIn(self.book2, result)
        self.assertNotIn(self.book1, result)

    def test_search_books_by_author(self):
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        result = self.library.search_books_by_author("Auteur test 2")
        self.assertIn(self.book2, result)
        self.assertNotIn(self.book1, result)

    def test_search_books_by_isbn(self):
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        result = self.library.search_books_by_isbn("2210765528")
        self.assertEqual(result, self.book1)
        result = self.library.search_books_by_isbn("140274577X")
        self.assertEqual(result, self.book2)
    
    def test_make_reservation(self):
        self.library.add_member(self.member)
        self.library.add_book(self.book1)
        reservation = self.library.make_reservation(self.member, self.book1)
        self.assertIn(reservation, self.library.reservations)
    
    def test_get_open_reservations(self):
        self.library.add_member(self.member)
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        reservation1 = self.library.make_reservation(self.member, self.book1)
        reservation2 = self.library.make_reservation(self.member, self.book2)
        reservations = self.library.get_open_reservations(self.member)
        self.assertIn(reservation1, reservations)
        self.assertIn(reservation2, reservations)
    
    def test(self):
        self.setUp()
        # Tests des méthodes locales
        self.test_add_book()
        self.test_search_books_by_title()
        self.test_search_books_by_author()
        self.test_search_books_by_isbn()
        self.test_update_book()
        self.test_remove_book()
        self.test_checkValid10CharsISBNCode()
        self.test_checkInvalid10CharsISBNCode()
        self.test_invalidLengthShouldThrowsException()
        self.test_nonNumericISBNThrowsException()
        self.test_checkISBNEndingWithAnXIsValid()
        self.test_checkValid13CharsISBNCode()
        # Tests des méthodes avec mock de connection DB
        self.test_get_all_books()

if __name__ == '__main__':
    unittest.main(exit=False)