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
        $scope.fields = [
              {name: 'cur_code', long_name: 'Code', pk: true}
            , {name: 'long_name', long_name: 'Name'}
            , {name: 'symbol'}
            , {name: 'shortcut'}
        ];

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

mod.directive('currency', function() {
    return {
          scope: { item: '=' }
        , templateUrl: 'partials/currency/currency-item.html'
    };
});

function capFirst(word) {
    return word.charAt(0).toUpperCase() + word.substr(1).toLowerCase();
}

function titleCase(str) {
    return str.replace(/\w\S*/g, capFirst);
}

function displayName(field) {
    if ('undefined' === typeof field.long_name)
        return titleCase(field.name);
    return field.long_name;
}

mod.directive('fieldEdit', function() {
    return {
          templateUrl: 'partials/generic/field-edit.html'
        , controller: ['$scope', function($scope) {
            $scope.readonly = false;
            $scope.displayname = displayName($scope.field);
            if ($scope.field.pk === true) {
                $scope.$watch ('edit_code', function(edit_code, _) {
                    $scope.readonly = (edit_code !== '');
                });
            }
        }],
    };
});

})();
