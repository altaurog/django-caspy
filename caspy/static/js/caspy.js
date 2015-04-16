(function(){
var mod = angular.module('caspy',
    ['ngRoute'
      , 'generic'
      , 'caspy.server'
      , 'caspy.currency'
      , 'caspy.book'
      , 'caspy.accounttype'
      , 'caspy.account'
    ]
);

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
                , controllerAs: 'listcontroller'
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
                , controllerAs: 'listcontroller'
                , resolve: {
                        currencies: ['CurrencyService',
                            function(CurrencyService) {
                                return CurrencyService.all();
                            }]
                    }
                , reloadOnSearch: false
            })
            .when('/accounttype/', {
                  templateUrl: 'partials/accounttype/accounttype-list.html'
                , controller: 'AccountTypeController'
                , controllerAs: 'listcontroller'
                , resolve: {
                        accounttypes: ['AccountTypeService',
                            function(AccountTypeService) {
                                return AccountTypeService.all();
                            }]
                    }
            })
            .when('/book/:book_id/account/', {
                  templateUrl: 'partials/account/account-list.html'
                , controller: 'AccountController'
                , controllerAs: 'listcontroller'
            })
            .otherwise({
                redirectTo: '/menu/'
            });
    }]);
})();
