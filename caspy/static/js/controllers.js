var caspyApp = angular.module('caspyApp', []);

caspyApp.controller('CurrencyController',
    ['$scope', '$http',
    function($scope, $http) {
        $http.get(apiRootUrl).success(function(data) {
            $http.get(data.currency).success(function(data) {
                $scope.currencies = data;
            });
        });
    }
]);
