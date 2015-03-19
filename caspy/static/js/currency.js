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
    ['$scope', 'currencies',
    function($scope, currencies) {
        $scope.currencies = currencies;
    }]
);

mod.controller('CurrencyDetailController',
    ['$scope', 'currency',
    function($scope, currency) {
        $scope.currency = currency;
    }]
);
})();
