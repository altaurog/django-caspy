(function(){
var mod = angular.module('caspy.accounttype', ['caspy.api', 'caspy.choice', 'generic']);

mod.factory('AccountTypeService', ['$q', 'ResourceWrapper', 'caspyAPI',
    function($q, ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('accounttype');
        return new ResourceWrapper(res, 'account_type');
    }]
);

mod.factory('AccountTypeChoiceService', ['$q', 'ChoiceService', 'AccountTypeService',
    function($q, ChoiceService, AccountTypeService) {
        function makeChoice(accounttype) {
            return [accounttype.account_type, accounttype.account_type];
        };
        return ChoiceService(AccountTypeService, makeChoice);
    }]
);

mod.controller('AccountTypeController',
    ['$injector', 'ListControllerMixin', 'AccountTypeService', 'accounttypes',
    function($injector, ListControllerMixin, AccountTypeService, accounttypes) {
        $injector.invoke(ListControllerMixin, this);
        this.dataservice = AccountTypeService;
        this.accounttypes = accounttypes;
        this.pk = 'account_type';
        var signChoices = [
            [true, "increase account balance"]
            , [false, "decrease account balance"]
        ];
        this.fields = [
              {name: 'account_type', pk: true}
            , {name: 'sign', long_name: 'Credits', choices: signChoices}
            , {name: 'credit_term'}
            , {name: 'debit_term'}
        ];
    }]
);

})();

