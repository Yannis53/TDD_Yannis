import unittest
import datetime
from isbn_validator import ISBNValidator
from main import Main
from book import Book
from member import Member

class Test(unittest.TestCase):

    def setUp(self):
        self.library = Main()
        self.book1 = Book("2210765528", "Livre test 1", "Auteur test 1", "Éditeur test 1", "Poche", True)
        self.book2 = Book("140274577X", "Livre test 2", "Auteur test 2", "Éditeur test 2", "BD", True)
        self.member = Member("Code1", "Yannis", "ZEMIRLINE", datetime.date(1993, 12, 15), "Homme")

    def test_add_book(self):
        self.library.add_book(self.book1)
        self.assertIn(self.book1, self.library.books)

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

    def test(self):
        self.setUp()
        self.test_add_book()
        self.test_checkValid10CharsISBNCode()
        self.test_checkInvalid10CharsISBNCode()
        self.test_invalidLengthShouldThrowsException()
        self.test_nonNumericISBNThrowsException()
        self.test_checkISBNEndingWithAnXIsValid()
        self.test_checkValid13CharsISBNCode()

if __name__ == '__main__':
    unittest.main(exit=False)