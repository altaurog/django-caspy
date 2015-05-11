(function(){
var mod = angular.module('caspy.account', ['caspy.api', 'generic']);

mod.factory('AccountService', ['$q', 'ResourceWrapper', 'caspyAPI',
    function($q, ResourceWrapper, caspyAPI) {
        return function(book_id) {
            var res = caspyAPI.get_resource('book_account', {'book_id': book_id});
            var as = new ResourceWrapper(res, 'account_id');
            as.choice = function(account) {
                return [account.account_id, account.path];
            };

            as.choices = function() {
                var d = $q.defer();
                this.all().then(function(all) {
                    all.$promise.then(
                        function(data) { d.resolve(data.map(as.choice)); },
                        function(message) { d.reject(message); }
                    );
                });
                return d.promise;
            }
            return as;
        };
    }]
);

mod.controller('AccountController'
    ,['$injector'
    , '$routeParams'
    , 'ListControllerMixin'
    , 'AccountService'
    , 'AccountTypeService'
    , 'CurrencyService'
    , function($injector
             , $routeParams
             , ListControllerMixin
             , AccountService
             , AccountTypeService
             , CurrencyService
        ) {
        $injector.invoke(ListControllerMixin, this);
        this.book_id = $routeParams['book_id'];
        this.dataservice = AccountService(this.book_id);
        this.assign('accounts', this.dataservice.all());
        this.pk = 'account_id';
        this.fields = [
              {i: -1, name: 'account_id', pk: true, hide: true}
            , {i: 0, name: 'name'}
            , {i: 2, name: 'description'}
        ];
        var ref = this;
        this.dataservice.choices().then(function(data) {
            ref.fields.push({i: 1, name: 'parent_id', choices: data});
            ref.sortFields();
        });
        AccountTypeService.choices().then(function(data) {
            ref.fields.push({i: 3, name: 'account_type', choices: data});
            ref.sortFields();
        });
        CurrencyService.choices().then(function(data) {
            ref.fields.push({i: 4, name: 'currency', choices: data});
            ref.sortFields();
        });
    }]
);

})();

