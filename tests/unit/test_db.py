import pytest
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from caspy import models

import testapp.models
from testapp import factories

pytestmark = pytest.mark.django_db()


class TestCurrency:
    def test_create_currency(self):
        currency = factories.CurrencyFactory()
        data = model_to_dict(currency)
        assert models.Currency.objects.filter(**data).exists()

    unique_fields = ('cur_code', 'shortcut', 'long_name')

    @pytest.mark.parametrize('dupfield', unique_fields)
    def test_uniquness(self, dupfield):
        data = {dupfield: 'A'}
        factories.CurrencyFactory(**data)
        with pytest.raises(IntegrityError):
            factories.CurrencyFactory(**data)


class TestBook:
    def test_create_book(self):
        book_obj = factories.BookFactory()
        data = model_to_dict(book_obj)
        assert models.Book.objects.filter(**data).exists()

    def test_uniqueness(self):
        name = 'Test Book'
        factories.BookFactory(name=name)
        with pytest.raises(IntegrityError):
            factories.BookFactory(name=name)


class TestAccountType:
    def test_create_accounttype(self):
        accounttype = factories.AccountTypeFactory()
        data = model_to_dict(accounttype)
        assert models.AccountType.objects.filter(**data).exists()

    def test_uniqueness(self):
        factories.AccountTypeFactory(account_type='Accounts Receivable')
        with pytest.raises(IntegrityError):
            factories.AccountTypeFactory(account_type='Accounts Receivable')


class TestAccount:
    def test_create_account(self):
        account_obj = factories.AccountFactory()
        data = model_to_dict(account_obj)
        assert models.Account.objects.filter(**data).exists()

    def test_create_with_empty_description(self):
        factories.AccountFactory(description='')

    def test_unique_id(self):
        account_obj = factories.AccountFactory()
        with pytest.raises(IntegrityError):
            factories.AccountFactory(account_id=account_obj.account_id)

    def test_unique_together(self):
        account_obj = factories.AccountFactory()
        name = account_obj.name
        book = account_obj.book
        factories.AccountFactory(name=name)
        factories.AccountFactory(book=book)
        with pytest.raises(IntegrityError):
            factories.AccountFactory(name=name, book=book)


class TestClosureTable:
    def test_self_path_created(self):
        a = factories.ThingFactory()
        assert testapp.models.ThingPath.objects.filter(
                    upper=a, lower=a, length=0,
                ).exists()

    def test_self_path_not_created_twice(self):
        factories.ThingFactory().save()

    def test_attach_leaf(self):
        a, b = factories.ThingFactory.create_batch(2)
        assert testapp.models.Thing.tree.attach(b, a) == 1
        assert testapp.models.ThingPath.objects.filter(
                    upper=a, lower=b, length=1,
                ).exists()

    def test_attach_branch(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        assert testapp.models.Thing.tree.attach(c, b) == 1
        assert testapp.models.Thing.tree.attach(b, a) == 2
        assert testapp.models.ThingPath.objects.filter(
                    upper=a, lower=c, length=2,
                ).exists()

    def test_get_paths(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        testapp.models.Thing.tree.attach(c, b)
        testapp.models.Thing.tree.attach(b, a)
        paths = testapp.models.Thing.tree.paths()
        assert paths == [[a], [a, b], [a, b, c]]

    def test_get_paths_with_qset(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        testapp.models.Thing.tree.attach(c, b)
        testapp.models.Thing.tree.attach(b, a)
        qset = testapp.models.Thing.objects.exclude(name=a.name)
        paths = testapp.models.Thing.tree.paths(qset)
        assert paths == [[b], [b, c]]

    def test_detach_leaf(self):
        a, b = factories.ThingFactory.create_batch(2)
        testapp.models.Thing.tree.attach(b, a)
        assert testapp.models.Thing.tree.detach(b) == 1
        assert not testapp.models.ThingPath.objects.filter(
                    upper=a, lower=b, length=1,
                ).exists()

    def test_detach_branch(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        testapp.models.Thing.tree.attach(c, b)
        testapp.models.Thing.tree.attach(b, a)
        assert testapp.models.Thing.tree.detach(b) == 2
        assert not testapp.models.ThingPath.objects.filter(
                    upper=a, lower=c, length=2,
                ).exists()

    def test_delete_middle_node(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        testapp.models.Thing.tree.attach(c, b)
        testapp.models.Thing.tree.attach(b, a)
        b.delete()
        assert not testapp.models.ThingPath.objects.filter(
                    upper=a, lower=c, length=2,
                ).exists()
