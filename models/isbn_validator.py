class ISBNValidator:
    LONG_ISBN_LENGTH = 13
    SHORT_ISBN_LENGTH = 10
    LONG_ISBN_DIVIDER = 10
    SHORT_ISBN_DIVIDER = 11

    def validateISBN(self, isbn):
        if len(isbn) == self.LONG_ISBN_LENGTH:
            return self.validateLongISBN(isbn)
        elif len(isbn) == self.SHORT_ISBN_LENGTH:
            return self.validateShortISBN(isbn)

        raise ValueError("An ISBN should be 10 or 13 characters long.")
    
    def validateLongISBN(self, isbn):
        total = sum(
            int(isbn[i]) if i % 2 == 0 else int(isbn[i]) * 3
            for i in range(self.LONG_ISBN_LENGTH)
        )
        return (total % self.LONG_ISBN_DIVIDER == 0)

    def validateShortISBN(self, isbn):
        total = 0

        for i in range(self.SHORT_ISBN_LENGTH):
            if not isbn[i].isdigit():
                if i != 9 or isbn[i] != 'X':
                    raise ValueError("An ISBN should contain digits only.")

                total += 10
                break
            total += int(isbn[i]) * (10 - i)

        return (total % self.SHORT_ISBN_DIVIDER == 0)