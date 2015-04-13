(function(){
var mod = angular.module('caspy.accounttype', ['caspy.api']);

mod.factory('AccountTypeService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('accounttype');
        return new ResourceWrapper(res, 'account_type');
    }]
);

mod.controller('AccountTypeController',
    ['$scope', 'AccountTypeService', 'accounttypes',
    function($scope, AccountTypeService, accounttypes) {
        $scope.dataservice = AccountTypeService;
        $scope.accounttypes = accounttypes;
        $scope.fields = [
              {name: 'account_type', pk: true}
            , {name: 'sign'}
            , {name: 'credit_term'}
            , {name: 'debit_term'}
        ];
    }]
);

})();

