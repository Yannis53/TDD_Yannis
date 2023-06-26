import unittest
from isbn_validator import ISBNValidator

class Test(unittest.TestCase):

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
        self.test_checkValid10CharsISBNCode()
        self.test_checkInvalid10CharsISBNCode()
        self.test_invalidLengthShouldThrowsException()
        self.test_nonNumericISBNThrowsException()
        self.test_checkISBNEndingWithAnXIsValid()
        self.test_checkValid13CharsISBNCode()

if __name__ == '__main__':
    unittest.main(exit=False)