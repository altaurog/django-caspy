# vim:fileencoding=utf-8
from __future__ import unicode_literals
from datetime import datetime
from caspy import models


def test_fixture():
    currency_objs = _load(models.Currency, currency_data)
    accounttype_objs = _load(models.AccountType, accounttype_data)
    book_objs = [models.Book.objects.create(**d) for d in book_data]
    income_kwargs = {
            'currency': currency_objs[0],
            'book': book_objs[0],
            'account_type': accounttype_objs[0],
        }
    income = create_account('Income', income_kwargs)
    salary = create_account('Salary', income_kwargs)
    models.Account.tree.attach(salary, income)
    tips = create_account('Tips', income_kwargs)
    citibank = models.Account.objects.create(
            name='Citibank',
            currency=currency_objs[0],
            book=book_objs[0],
            account_type=accounttype_objs[1],
            description='Citibank Test Account',
        )
    chase = models.Account.objects.create(
            name='Chase',
            currency=currency_objs[1],
            book=book_objs[1],
            account_type=accounttype_objs[1],
        )
    return {
            'currencies': currency_objs,
            'accounttypes': accounttype_objs,
            'books': book_objs,
            'accounts': [income, salary, tips, citibank, chase],
        }


def _load(django_model, data):
    objs = [django_model(**d) for d in data]
    django_model.objects.bulk_create(objs)
    return objs


def create_account(name, kwargs):
    desc = name + ' Test Account'
    return models.Account.objects.create(name=name, description=desc, **kwargs)


currency_data = [
        {
            'cur_code': 'USD',
            'shortcut': '$',
            'symbol': '$',
            'long_name': 'US Dollar',
        },
        {
            'cur_code': 'CAD',
            'long_name': 'Canadian Dollar',
            'symbol': '$',
            'shortcut': 'C',
        },
        {
            'pk': 'EUR',
            'long_name': 'Euro',
            'symbol': '€',
            'shortcut': 'E',
        },
    ]

accounttype_data = [
        {
            'account_type': 'Income',
            'sign': True,
            'credit_term': 'income',
            'debit_term': 'expense',
        },
        {
            'account_type': 'Bank Account',
            'sign': False,
            'credit_term': 'withdraw',
            'debit_term': 'deposit',
        },
    ]

book_data = [
        {'name': 'Test Book 1', 'created_at': datetime(2015, 7, 22, 15)},
        {'name': 'Test Book 2', 'created_at': datetime(2015, 7, 22, 16)},
    ]
