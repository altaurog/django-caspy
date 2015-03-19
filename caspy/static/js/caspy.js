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
                  templateUrl: proot + 'book-list.html'
                , controller: 'BookController'
                , resolve: {
                        books: ['BookService',
                            function(BookService) {
                                return BookService.all();
                            }]
                    }
            })
            .when('/book/new/', {
                  templateUrl: proot + 'book-edit.html'
                , controller: 'BookEditController'
            })
            .when('/book/:book_id/', {
                  templateUrl: proot + 'book-detail.html'
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
                  templateUrl: proot + 'currency-list.html'
                , controller: 'CurrencyController'
                , resolve: {
                        currencies: ['CurrencyService',
                            function(CurrencyService) {
                                return CurrencyService.all();
                            }]
                    }
            })
            .when('/currency/new/', {
                  templateUrl: proot + 'currency-edit.html'
                , controller: 'CurrencyEditController'
            })
            .when('/currency/:code/', {
                  templateUrl: proot + 'currency-detail.html'
                , controller: 'CurrencyDetailController'
                , resolve: {
                        currency: ['$route', 'CurrencyService',
                            function($route, CurrencyService) {
                                var code = $route.current.params.code;
                                return CurrencyService.get(code);
                            }]
                    }
            })
            .otherwise({
                redirectTo: '/menu/'
            });
    }]);
})();
