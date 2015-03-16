var mod = angular.module('caspy.currency', ['caspy.api']);

mod.controller('CurrencyController',
    ['$scope', '$http', 'caspyAPI',
    function($scope, $http, caspyAPI) {
        caspyAPI.endpoint('currency', function(endpoint) {
            $http.get(endpoint).success(function(data) {
                $scope.currencies = data;
            });
        });
    }]
);
