(function(){
var mod = angular.module('caspy.currency', ['caspy.api']);

mod.controller('CurrencyController',
    ['$scope', '$http', 'caspyAPI',
    function($scope, $http, caspyAPI) {
        caspyAPI.get_endpoint('currency')
            .then($http.get)
            .then(function(response) {
                $scope.currencies = response.data;
            }).catch(function(response) {
                console.log(response);
            });
    }]
);
})();
