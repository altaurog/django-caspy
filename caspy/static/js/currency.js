(function(){
var mod = angular.module('caspy.currency', ['caspy.api']);

mod.controller('CurrencyController',
    ['$scope', 'caspyAPI',
    function($scope, caspyAPI) {
        caspyAPI.get_resource('currency')
            .then(function(resource) {
                $scope.currencies = resource.query();
            });
    }]
);

mod.controller('CurrencyDetailController',
    ['$scope', '$routeParams','caspyAPI',
    function($scope, $routeParams, caspyAPI) {
        caspyAPI.get_resource('currency')
            .then(function(resource) {
                $scope.currency = resource.get({code: $routeParams.code});
            });
    }]
);
})();
