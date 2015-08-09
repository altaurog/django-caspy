(function(){
var mod = angular.module('caspy.account', ['caspy.api', 'caspy.choice', 'generic', 'MassAutoComplete']);

mod.factory('AccountService', ['$q', 'ResourceWrapper', 'caspyAPI',
    function($q, ResourceWrapper, caspyAPI) {
        return function(book_id) {
            var res = caspyAPI.get_resource('account', {'book_id': book_id});
            return new ResourceWrapper(res, 'account_id');
        };
    }]
);

mod.factory('AccountChoiceService', ['$q', '$sce', 'ChoiceService', 'AccountService',
    function($q, $sce, ChoiceService, AccountService) {
        function makeChoice(account) {
            return [account.account_id, account.path];
        };

        return function(book_id) {
            var dataservice = AccountService(book_id);
            var cs = ChoiceService(dataservice, makeChoice);

            cs.suggest = function(text) {
                var re = makeRegex(text);
                return cs.data.then(function(data) {
                    var s = [];
                    data.forEach(function(account) {
                        if (re.test(account.path))
                            s.push({
                                  id: account.account_id
                                , value: account.path
                                , label: $sce.trustAsHtml(account.path)
                            });
                    });
                    return s;
                });
            };
            return cs;
        }
    }]
);

function subFunc(c) {
    if ('\\^$*+?.()|{}[]'.indexOf(c) >= 0)
        return '\\' + c
    return c
}

function makeRegex(search) {
    return new RegExp(search.split('').map(subFunc).join('.*'), 'i');
}

mod.controller('AccountController'
    ,['$injector'
    , '$routeParams'
    , '$q'
    , 'ListControllerMixin'
    , 'AccountService'
    , 'AccountChoiceService'
    , 'AccountTypeChoiceService'
    , 'CurrencyChoiceService'
    , function($injector
             , $routeParams
             , $q
             , ListControllerMixin
             , AccountService
             , AccountChoiceService
             , AccountTypeChoiceService
             , CurrencyChoiceService
        ) {
        $injector.invoke(ListControllerMixin, this);
        var ref = this;
        this.book_id = $routeParams['book_id'];
        this.dataservice = AccountService(this.book_id);
        this.assign('accounts', this.dataservice.all().then(parentPath));
        this.pk = 'account_id';
        this.onParentSelect = function(obj) {
            console.log(obj);
            ref.edititem.parent_id = obj.id;
        };
        this.accountchoiceservice = AccountChoiceService(this.book_id);
        this.parent_ac = {
              suggest: this.accountchoiceservice.suggest
            , on_select: this.onParentSelect
        };
        this.fields = [
              {i: -1, name: 'account_id', pk: true, hide: true}
            , {i: 0, name: 'name'}
            , {i: 1, name: 'parent', autocomplete: this.parent_ac}
            , {i: 2, name: 'description'}
        ];
        this.choiceFields([
            , [3, 'account_type', AccountTypeChoiceService.choices]
            , [4, 'currency', CurrencyChoiceService.choices]
        ]);
    }]
);

function parentPath(p) {
    return p.$promise.then(function(data) {
        data.forEach(function(account) {
            account.parent = account.path.replace(/(^|::)[^:]+$/, '');
        });
        return data;
    });
}

})();

