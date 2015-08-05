from caspy.domain import command, models


class TestBook:
    def test_prepare_new_book(self):
        empty_book = models.Book()
        result = command.prepare_book(empty_book, 'now')
        assert isinstance(result, models.Book)
        assert result.created_at == 'now'

    def test_prepare_old_book(self):
        dated_book = models.Book(created_at='last week')
        result = command.prepare_book(dated_book, 'now')
        assert isinstance(result, models.Book)
        assert result.created_at == 'last week'


class TestTransaction:
    def test_sort_transactions(self):
        a = models.Transaction(date=1)
        b = models.Transaction(date=2)
        assert command.sort_transactions([b, a]) == [a, b]
