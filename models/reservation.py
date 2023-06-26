class Reservation:
    def __init__(self, reservation_id, member_id, limit_date, isbn_book):
        self.reservation_id = reservation_id
        self.member_id = member_id
        self.limit_date = limit_date
        self.isbn_book = isbn_book
        self.return_date = None
        self.is_returned = False