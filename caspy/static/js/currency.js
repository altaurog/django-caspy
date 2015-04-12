(function(){
var mod = angular.module('caspy.currency', ['caspy.api']);

mod.factory('CurrencyService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('currency');
        return new ResourceWrapper(res, 'cur_code');
    }]
);

mod.controller('CurrencyController',
    ['$scope', '$route', '$location', 'CurrencyService', 'currencies',
    function($scope, $route, $location, CurrencyService, currencies) {
        $scope.currencies = currencies;
        var selected = $location.hash();
        if (selected) {
            currencies.$promise.then(function(data) {
                angular.forEach(data, function(currency, i) {
                    if (currency.cur_code === selected) {
                        $scope.select(currency);
                    }
                });
            });
        }

        $scope.select = function(currency) {
            $location.hash(currency.cur_code);
            $scope.currency = currency;
            $scope.edit_code = currency.cur_code;
        };

        $scope.add = function() {
            $scope.currency = {};
            $scope.edit_code = '';
        }

        $scope.close = function() {
            $scope.currency = null;
            $scope.edit_code = null;
            $location.hash('');
        }

        $scope.save = function() {
            var p;
            if ($scope.edit_code)
                p = CurrencyService.update($scope.edit_code, $scope.currency);
            else
                p = CurrencyService.create($scope.currency);
            p.then(function(obj) {
                $location.hash('');
                $route.reload();
            });
        };

        $scope.delete = function() {
            if ($scope.edit_code) {
                CurrencyService.del($scope.edit_code)
                    .then(function(obj) {
                        $location.hash('');
                        $route.reload();
                    });
            }
        };
    }]
);

})();
