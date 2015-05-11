(function(){
var mod = angular.module('caspy.accounttype', ['caspy.api', 'generic']);

mod.factory('AccountTypeService', ['$q', 'ResourceWrapper', 'caspyAPI',
    function($q, ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('accounttype');
        var ats = new ResourceWrapper(res, 'account_type');

        ats.choice = function(accounttype) {
            return [accounttype.account_type, accounttype.account_type];
        };

        ats.choices = function() {
            var d = $q.defer();
            this.all().then(function(all) {
                all.$promise.then(
                    function(data) { d.resolve(data.map(ats.choice)); },
                    function(message) { d.reject(message); }
                );
            });
            return d.promise;
        }
        return ats;
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

