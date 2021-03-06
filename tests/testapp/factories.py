from datetime import datetime, timedelta
import factory
from caspy import models, time
from .models import Thing


def letterstr(size, extra=''):
    return lambda n: size * chr(65 + n % 25) + extra


def datetimeseq(n):
    return time.utc.localize(datetime(2015, 1, 1) + timedelta(minutes=10) * n)


class CurrencyFactory(factory.DjangoModelFactory):
    cur_code = factory.Sequence(letterstr(3))
    shortcut = factory.Sequence(letterstr(1))
    symbol = factory.Sequence(letterstr(1))
    long_name = factory.Sequence(letterstr(1, ' Currency'))

    class Meta:
        model = models.Currency


class BookFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Test Book %d' % n)
    created_at = factory.Sequence(datetimeseq)

    class Meta:
        model = models.Book


class AccountTypeFactory(factory.DjangoModelFactory):
    account_type = factory.Iterator(
                        ['Credit Card', 'Bank Account', 'Income', 'Expense'])
    sign = factory.Iterator([True, False])
    credit_term = factory.Iterator(['charge', 'withdraw', 'income', 'credit'])
    debit_term = factory.Iterator(['payment', 'deposit', 'expense', 'debit'])

    class Meta:
        model = models.AccountType


class AccountFactory(factory.DjangoModelFactory):
    name = factory.Iterator(['Citibank Visa', 'Chase', 'Walmart', 'Rent'])
    book = factory.SubFactory(BookFactory)
    account_type = factory.SubFactory(AccountTypeFactory)
    currency = factory.SubFactory(CurrencyFactory)

    @factory.lazy_attribute
    def description(self):
        return self.name + ' account'

    class Meta:
        model = models.Account


class ThingFactory(factory.DjangoModelFactory):
    "Dummy model factory for testing closure table"
    name = factory.Sequence(letterstr(1))
    tgroup = 1

    class Meta:
        model = Thing
