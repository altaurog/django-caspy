(function(){
var mod = angular.module('caspy.account', ['caspy.api', 'caspy.choice', 'generic']);

mod.factory('AccountService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        return function(book_id) {
            var res = caspyAPI.get_resource('account', {'book_id': book_id});
            return new ResourceWrapper(res, 'account_id');
        };
    }]
);

mod.factory('AccountChoiceService', ['$q', 'ChoiceService', 'AccountService',
    function($q, ChoiceService, AccountService) {
        function makeChoice(account) {
            return [account.account_id, account.path];
        };

        return function(book_id) {
            var dataservice = AccountService(book_id);
            var cs = ChoiceService(dataservice, makeChoice);

            cs.dataservice = dataservice;
            cs.all = function() {
                return $q.all([cs.data, cs.choices]).then(function(p) {
                    var data = p[0];
                    data.forEach(function(account) {
                        if (account.parent_id)
                            account.parentPath = cs.lookup(account.parent_id);
                        else
                            account.parentPath = '';
                    });
                    return data;
                });
            }
            return cs;
        }
    }]
);

mod.controller('AccountController'
    ,['$injector'
    , '$routeParams'
    , 'ListControllerMixin'
    , 'AccountChoiceService'
    , 'AccountTypeChoiceService'
    , 'CurrencyChoiceService'
    , function($injector
             , $routeParams
             , ListControllerMixin
             , AccountChoiceService
             , AccountTypeChoiceService
             , CurrencyChoiceService
        ) {
        $injector.invoke(ListControllerMixin, this);
        var ref = this;
        this.book_id = $routeParams['book_id'];
        this.accountchoiceservice = AccountChoiceService(this.book_id);
        this.assign('accounts', this.accountchoiceservice.all());
        this.dataservice = this.accountchoiceservice.dataservice;
        this.pk = 'account_id';
        this.fields = [
              {i: -1, name: 'account_id', pk: true, hide: true}
            , {i: 0, name: 'name'}
            , {i: 2, name: 'description'}
        ];
        this.choiceFields([
            , [1, 'parent_id', this.accountchoiceservice.choices]
            , [3, 'account_type', AccountTypeChoiceService.choices]
            , [4, 'currency', CurrencyChoiceService.choices]
        ]);
        this.newitem = function() {
            return {
                  account_id: ''
                , name: ''
                , description: ''
                , parent_id: null
                , account_type: ''
                , currency: ''
            };
        };
    }]
);

})();
