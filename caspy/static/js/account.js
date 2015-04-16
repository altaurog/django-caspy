(function(){
var mod = angular.module('caspy.account', ['caspy.api', 'generic']);

mod.factory('AccountService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        return function(book_id) {
            var res = caspyAPI.get_resource('book_account', {'book_id': book_id});
            return new ResourceWrapper(res, 'account_id');
        };
    }]
);

mod.controller('AccountController',
    ['$injector', '$routeParams', 'ListControllerMixin', 'AccountService',
    function($injector, $routeParams, ListControllerMixin, AccountService) {
        $injector.invoke(ListControllerMixin, this);
        this.book_id = $routeParams['book_id'];
        this.dataservice = AccountService(this.book_id);
        this.assign('accounts', this.dataservice.all());
        this.pk = 'account_id';
        this.fields = [
              {name: 'account_id', pk: true, hide: true}
            , {name: 'path'}
            , {name: 'description'}
            , {name: 'account_type'}
            , {name: 'currency'}
        ];
    }]
);

})();

