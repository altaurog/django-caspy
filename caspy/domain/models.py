from caspy.lw import Lightweight as Base
from caspy import str


class Currency(Base):
    _fields = 'cur_code', 'shortcut', 'symbol', 'long_name'


class Book(Base):
    _fields = 'book_id', 'name', 'created_at'

    def __str__(self):
        return str(self.name)


class AccountType(Base):
    _fields = 'account_type', 'sign', 'credit_term', 'debit_term'


class Account(Base):
    _fields = ('account_id', 'name', 'book', 'account_type',
               'currency', 'description')
