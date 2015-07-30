(function(){
var mod = angular.module('caspy.account', ['caspy.api', 'generic', 'MassAutoComplete']);

mod.factory('AccountService', ['$q', 'ResourceWrapper', 'caspyAPI',
    function($q, ResourceWrapper, caspyAPI) {
        return function(book_id) {
            function makeChoice(account) {
                return [account.account_id, account.path];
            };
            var res = caspyAPI.get_resource('account', {'book_id': book_id});
            return new ResourceWrapper(res, 'account_id', makeChoice);
        };
    }]
);

mod.controller('AccountController'
    ,['$injector'
    , '$routeParams'
    , '$q'
    , '$sce'
    , 'ListControllerMixin'
    , 'AccountService'
    , 'AccountTypeService'
    , 'CurrencyService'
    , function($injector
             , $routeParams
             , $q
             , $sce
             , ListControllerMixin
             , AccountService
             , AccountTypeService
             , CurrencyService
        ) {
        $injector.invoke(ListControllerMixin, this);
        var ref = this;
        this.book_id = $routeParams['book_id'];
        this.dataservice = AccountService(this.book_id);
        this.assign('accounts', this.dataservice.all().then(parentPath));
        this.pk = 'account_id';
        this.suggestParentAccount = function(text) {
            var re = makeRegex(text);
            var s = [];
            ref.accounts.forEach(function(account) {
                if (re.test(account.path))
                    s.push({
                          id: account.account_id
                        , value: account.path
                        , label: $sce.trustAsHtml(account.path)
                    });
            });
            return s;
        };
        this.onParentSelect = function(obj) {
            console.log(obj);
            ref.edititem.parent_id = obj.id;
        };
        this.parent_ac = {
              suggest: this.suggestParentAccount
            , on_select: this.onParentSelect
        };
        this.fields = [
              {i: -1, name: 'account_id', pk: true, hide: true}
            , {i: 0, name: 'name'}
            , {i: 1, name: 'parent', autocomplete: this.parent_ac}
            , {i: 2, name: 'description'}
        ];
        this.choiceFields([
            , [3, 'account_type', AccountTypeService.choices()]
            , [4, 'currency', CurrencyService.choices()]
        ]);
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

function parentPath(p) {
    return p.$promise.then(function(data) {
        data.forEach(function(account) {
            account.parent = account.path.replace(/(^|::)[^:]+$/, '');
        });
        return data;
    });
}

})();

