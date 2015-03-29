(function(){
var mod = angular.module('caspy',
    ['ngRoute', 'caspy.server', 'caspy.currency', 'caspy.book']);

mod.config(['$httpProvider', '$routeProvider', 'Constants',
    function($httpProvider, $routeProvider, Constants){
        // tell angular where to find template partials
        $httpProvider.interceptors.push(function($q) {
            return {
                request: function(request) {
                    request.url = request.url.replace(
                                    /^partials\//,
                                    Constants.partialsRoot
                                );
                    return request || $q.when(request);
                }
            };
        });

        $routeProvider
            .when('/menu/', {
                  templateUrl: 'partials/menu.html'
            })
            .when('/book/', {
                  templateUrl: 'partials/book/book-list.html'
                , controller: 'BookController'
                , resolve: {
                        books: ['BookService',
                            function(BookService) {
                                return BookService.all();
                            }]
                    }
            })
            .when('/book/new/', {
                  templateUrl: 'partials/book/book-edit.html'
                , controller: 'BookEditController'
            })
            .when('/book/:book_id/', {
                  templateUrl: 'partials/book/book-detail.html'
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
                  templateUrl: 'partials/currency/currency-list.html'
                , controller: 'CurrencyController'
                , resolve: {
                        currencies: ['CurrencyService',
                            function(CurrencyService) {
                                return CurrencyService.all();
                            }]
                    }
                , reloadOnSearch: false
            })
            .when('/currency/new/', {
                  templateUrl: 'partials/currency/currency-edit.html'
                , controller: 'CurrencyEditController'
            })
            .when('/currency/:cur_code/', {
                  templateUrl: 'partials/currency/currency-detail.html'
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
