(function(){
var mod = angular.module('caspy',
    ['ngRoute', 'caspy.server', 'caspy.currency']);

mod.config(['$routeProvider', 'Constants',
    function($routeProvider, Constants){
        var proot = Constants.partialsRoot;
        $routeProvider
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
                redirectTo: '/currency/'
            });
    }]);
})();
