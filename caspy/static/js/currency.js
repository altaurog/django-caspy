(function(){
var mod = angular.module('caspy.currency', ['caspy.api']);

mod.factory('CurrencyService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('currency');
        return new ResourceWrapper(res, 'code');
    }]
);

mod.controller('CurrencyController',
    ['$scope', 'currencies',
    function($scope, currencies) {
        $scope.currencies = currencies;
    }]
);

mod.controller('CurrencyDetailController',
    ['$scope', '$location', 'CurrencyService', 'currency',
    function($scope, $location, CurrencyService, currency) {
        $scope.currency = currency;
        $scope.del = function(){
            return CurrencyService.del($scope.currency.code)
                .then(function() { $location.path('/currency/'); });
        };
    }]
);

mod.controller('CurrencyEditController',
    ['$scope', '$location', 'CurrencyService',
    function($scope, $location, CurrencyService) {
        $scope.save = function() {
            return CurrencyService.save($scope.currency)
                .then(function() { $location.path('/currency/'); });
        };
    }]
);

})();
