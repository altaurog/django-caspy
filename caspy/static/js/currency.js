(function(){
var mod = angular.module('caspy.currency', ['caspy.api']);

mod.factory('CurrencyService', ['$q', 'caspyAPI',
    function($q, caspyAPI) {
        var cs;
        var res = caspyAPI.get_resource('currency');
        function rc(fcn) { return res.then(fcn); }
        return cs = {
              all: function() {
                return rc(function(res) { return res.query(); });
                }
            , get: function(code) {
                return rc(function(res) { return res.get({code: code}); });
                }
            , save: function(currency) {
                return rc(function(res) { return res.save(currency); });
                }
            , del: function(code) {
                return rc(function(res) { return res.delete({code: code}); });
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
