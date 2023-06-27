class ISBNValidator:

    def validateISBN(self, isbn):
        if len(isbn) == 13:
            return self.validateLongISBN(isbn)
        elif len(isbn) == 10:
            return self.validateShortISBN(isbn)

        raise ValueError("An ISBN should be 10 or 13 characters long.")
    
    def validateLongISBN(self, isbn):
        total = sum(
            int(isbn[i]) if i % 2 == 0 else int(isbn[i]) * 3
            for i in range(13)
        )
        return (total % 10 == 0)

    def validateShortISBN(self, isbn):
        total = 0

        for i in range(10):
            if not isbn[i].isdigit():
                if i != 9 or isbn[i] != 'X':
                    raise ValueError("An ISBN should contain digits only.")

                total += 10
                break
            total += int(isbn[i]) * (10 - i)

        return (total % 11 == 0)