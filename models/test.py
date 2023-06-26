import unittest
from isbn_validator import ISBNValidator

class Test(unittest.TestCase):

    def test_checkValid10CharsISBNCode(self):
        validator = ISBNValidator()
        result = validator.validateISBN("2210765528")
        self.assertTrue(result, "first assertion")
        result = validator.validateISBN("2226392122")
        self.assertTrue(result, "second assertion")

    def test(self):
        self.test_checkValid10CharsISBNCode()

if __name__ == '__main__':
    unittest.main(exit=False)