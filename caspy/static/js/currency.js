(function(){
var mod = angular.module('caspy.currency', ['caspy.api']);

mod.factory('CurrencyService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('currency');
        return new ResourceWrapper(res, 'cur_code');
    }]
);

mod.controller('CurrencyController',
    ['$scope', 'CurrencyService', 'currencies',
    function($scope, CurrencyService, currencies) {
        $scope.dataservice = CurrencyService;
        $scope.currencies = currencies;
        $scope.fields = [
              {name: 'cur_code', long_name: 'Code', pk: true}
            , {name: 'long_name', long_name: 'Name'}
            , {name: 'symbol'}
            , {name: 'shortcut'}
        ];
    }]
);

})();
