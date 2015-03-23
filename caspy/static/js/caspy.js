(function(){
var mod = angular.module('caspy',
    ['ngRoute', 'caspy.server', 'caspy.currency', 'caspy.book']);

mod.config(['$routeProvider', 'Constants',
    function($routeProvider, Constants){
        var proot = Constants.partialsRoot;
        $routeProvider
            .when('/menu/', {
                  templateUrl: proot + 'menu.html'
            })
            .when('/book/', {
                  templateUrl: proot + 'book/book-list.html'
                , controller: 'BookController'
                , resolve: {
                        books: ['BookService',
                            function(BookService) {
                                return BookService.all();
                            }]
                    }
            })
            .when('/book/new/', {
                  templateUrl: proot + 'book/book-edit.html'
                , controller: 'BookEditController'
            })
            .when('/book/:book_id/', {
                  templateUrl: proot + 'book/book-detail.html'
                , controller: 'BookDetailController'
                , resolve: {
                        book: ['$route', 'BookService',
                            function($route, BookService) {
                                var book_id = $route.current.params.book_id;
                                return BookService.get(book_id);
                            }]
                    }
            })
            .when('/currency/', {
                  templateUrl: proot + 'currency/currency-list.html'
                , controller: 'CurrencyController'
                , resolve: {
                        currencies: ['CurrencyService',
                            function(CurrencyService) {
                                return CurrencyService.all();
                            }]
                    }
            })
            .when('/currency/new/', {
                  templateUrl: proot + 'currency/currency-edit.html'
                , controller: 'CurrencyEditController'
            })
            .when('/currency/:cur_code/', {
                  templateUrl: proot + 'currency/currency-detail.html'
                , controller: 'CurrencyDetailController'
                , resolve: {
                        currency: ['$route', 'CurrencyService',
                            function($route, CurrencyService) {
                                var cur_code = $route.current.params.cur_code;
                                return CurrencyService.get(cur_code);
                            }]
                    }
            })
            .otherwise({
                redirectTo: '/menu/'
            });
    }]);
})();
