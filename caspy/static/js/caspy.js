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
            .otherwise({
                redirectTo: '/currency/'
            });
    }]);
})();
