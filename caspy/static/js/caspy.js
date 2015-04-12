(function(){
var mod = angular.module('caspy',
    ['ngRoute', 'generic', 'caspy.server', 'caspy.currency', 'caspy.book']);

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
            .otherwise({
                redirectTo: '/menu/'
            });
    }]);
})();
