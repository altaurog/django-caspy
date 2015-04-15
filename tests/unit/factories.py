import factory
from caspy import models


def letterstr(size, extra=''):
    return lambda n: size * chr(65 + n) + extra


class CurrencyFactory(factory.DjangoModelFactory):
    cur_code = factory.Sequence(letterstr(3))
    shortcut = factory.Sequence(letterstr(1))
    symbol = factory.Sequence(letterstr(1))
    long_name = factory.Sequence(letterstr(1, ' Currency'))

    class Meta:
        model = models.Currency


class BookFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Test Book %d' % n)

    class Meta:
        model = models.Book


class AccountTypeFactory(factory.DjangoModelFactory):
    account_type = factory.Iterator(
                        ['Credit Card', 'Bank Account', 'Income', 'Expense'])
    sign = factory.Iterator([True, False])
    credit_term = factory.Iterator(['charge', 'withdraw', 'income', 'credit'])
    debit_term = factory.Iterator(['payment', 'deposit', 'income', 'debit'])

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
