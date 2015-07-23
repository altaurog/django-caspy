# vim:fileencoding=utf-8
from __future__ import unicode_literals
from datetime import datetime, date
from caspy import models, time


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
    asset_kwargs = income_kwargs.copy()
    asset_kwargs['account_type'] = accounttype_objs[1]
    citibank = create_account('Citibank', asset_kwargs)
    asset2_kwargs = {
            'currency': currency_objs[1],
            'book': book_objs[1],
            'account_type': accounttype_objs[1],
        }
    chase = create_account('Chase', asset2_kwargs)
    create_transactions(salary, tips, citibank)
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


def create_transactions(*accounts):
    for xdata in transaction_data:
        xact = models.Transaction.objects.create(
                date=xdata['date'],
                description=xdata['description'],
            )
        for sdata in xdata['splits']:
            xact.split_set.create(
                    number=sdata['number'],
                    account=find(sdata['account'], accounts),
                    status=sdata['status'],
                    amount=sdata['amount'],
                    description=sdata.get('description', ''),
                )


def find(account_name, accounts):
    for a in accounts:
        if a.name == account_name:
            return a


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
            'sign': False,
            'credit_term': 'income',
            'debit_term': 'expense',
        },
        {
            'account_type': 'Bank Account',
            'sign': True,
            'credit_term': 'withdraw',
            'debit_term': 'deposit',
        },
    ]

transaction_data = [
        {
            'date': date(2015, 6, 28),
            'description': 'Payday',
            'splits': [
                {
                    'number': '100',
                    'account': 'Salary',
                    'status': 'c',
                    'amount': -8000,
                },
                {
                    'number': '1339',
                    'account': 'Citibank',
                    'status': 'c',
                    'amount': 8000,
                },
            ],
        },
        {
            'date': date(2015, 7, 3),
            'description': 'Tips w/dl',
            'splits': [
                {
                    'number': '129',
                    'account': 'Tips',
                    'status': 'n',
                    'amount': -837,
                },
                {
                    'number': '1345',
                    'account': 'Citibank',
                    'status': 'n',
                    'amount': 837,
                },
            ],
        },
    ]

u = time.utc.localize

book_data = [
        {'name': 'Test Book 1', 'created_at': u(datetime(2015, 7, 22, 15))},
        {'name': 'Test Book 2', 'created_at': u(datetime(2015, 7, 22, 16))},
    ]
