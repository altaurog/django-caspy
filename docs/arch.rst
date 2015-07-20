Architecture and Technical Design
==================================

We achieve better testing coverage and separation of concerns by minimizing
reliance on django ORM integration.  We use very lightweight (call them
anemic if you like) business objects and a functional, DDD approach.

We are not as overly preoccupied with DRY as django, particularly with
regards to the names of data fields.

The layers, roughly:

    angular controllers
    angular resources
     |
    django view routing
    django rest framework
    serializers
    business objects
    command layer
    query layer
    orm adaptor
    django orm
     |
    database


External API
=============

Root
----

GET
    API root provides endpoint template lookups by name

Currency List
-------------

GET
    List all currencies

POST
    Add a currency

Currency Detail
---------------

GET
    Get a single currency

PUT
    Update currency

DELETE
    Delete currency

Account Type List
------------------

GET
    List all account types

POST
    Add a account type

Account Type Detail
--------------------

GET
    Get a single account type

PUT
    Update account type

DELETE
    Delete account type

Book List
-------------

GET
    List all books

POST
    Add a book

Book Detail
---------------

GET
    Get a single book

PUT
    Update book

DELETE
    Delete book

Account List
--------------
GET
    List all accounts for a given book.  Book id required.

POST
    Add an account to a book.  Book id required.

Account Detail
--------------
GET
    Get single account.  Book id and Account id required.

PUT
    Update book

DELETE
    Delete account and all its transactions.  Sub accounts become children
    of the parent account.

Account Merge
-------------
POST
    Merge account and its transactions into a different account

Transaction List
----------------
GET
    List all transactions for given book.  Book id required.
    Optional account filter.

POST
    Add new transaction to given book.  Book id required.

Transaction Detail
------------------
GET
    Get single transaction.  Book id required.

PUT
    Update transaction

DELETE
    Delete transaction
