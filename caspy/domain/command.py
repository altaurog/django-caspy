def prepare_book(book, now):
    created_at = book.created_at or now
    return book.copy(created_at=created_at)
