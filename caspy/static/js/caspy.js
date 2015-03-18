(function(){
var mod = angular.module('caspy',
    ['ngRoute', 'caspy.server', 'caspy.currency']);

mod.config(['$routeProvider', 'Constants',
    function($routeProvider, Constants){
        var proot = Constants.partialsRoot;
        $routeProvider
            .when('/currency/', {
                templateUrl: proot + 'currency-list.html',
                controller: 'CurrencyController'
            })
            .when('/currency/:code/', {
                templateUrl: proot + 'currency-detail.html',
                controller: 'CurrencyDetailController'
            })
            .otherwise({
                redirectTo: '/currency/'
            });
    }]);
})();
