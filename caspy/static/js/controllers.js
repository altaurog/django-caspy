var caspyApp = angular.module('caspyApp');

caspyApp.controller('CurrencyController',
    ['$scope', '$http', 'caspyAPI',
    function($scope, $http, caspyAPI) {
        caspyAPI.endpoint('currency', function(endpoint) {
            $http.get(endpoint).success(function(data) {
                $scope.currencies = data;
            });
        });
    }]
);
