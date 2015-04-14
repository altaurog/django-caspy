(function(){
var mod = angular.module('caspy.accounttype', ['caspy.api', 'generic']);

mod.factory('AccountTypeService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('accounttype');
        return new ResourceWrapper(res, 'account_type');
    }]
);

mod.controller('AccountTypeController',
    ['$injector', 'ListControllerMixin', 'AccountTypeService', 'accounttypes',
    function($injector, ListControllerMixin, AccountTypeService, accounttypes) {
        $injector.invoke(ListControllerMixin, this);
        this.dataservice = AccountTypeService;
        this.accounttypes = accounttypes;
        this.pk = 'account_type';
        this.fields = [
              {name: 'account_type', pk: true}
            , {name: 'sign'}
            , {name: 'credit_term'}
            , {name: 'debit_term'}
        ];
    }]
);

})();

