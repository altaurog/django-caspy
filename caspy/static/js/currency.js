(function(){
var mod = angular.module('caspy.currency', ['caspy.api']);

mod.factory('CurrencyService', ['$q', 'caspyAPI',
    function($q, caspyAPI) {
        var cur_service;
        return cur_service = {
              all: function() {
                    return caspyAPI.get_resource('currency')
                        .then(function(resource){
                            return resource.query();
                        });
                }
            , get: function(code) {
                    return caspyAPI.get_resource('currency')
                        .then(function(resource){
                            return resource.get({code: code});
                        });
                }
            };
    }]
);

mod.controller('CurrencyController',
    ['$scope', 'CurrencyService',
    function($scope, CurrencyService) {
        CurrencyService.all().then(function(data) {
            $scope.currencies = data;
        });
    }]
);

mod.controller('CurrencyDetailController',
    ['$scope', '$routeParams','CurrencyService',
    function($scope, $routeParams, CurrencyService) {
        CurrencyService.get($routeParams.code).then(function(data) {
            $scope.currency = data;
        });
    }]
);
})();
