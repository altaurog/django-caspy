(function(){
var mod = angular.module('caspy.book', ['caspy.api', 'generic']);

mod.factory('BookService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('book');
        return new ResourceWrapper(res, 'book_id');
    }]
);

mod.controller('BookController',
    ['$injector', 'ListControllerMixin', 'BookService', 'books',
    function($injector, ListControllerMixin, BookService, books) {
        $injector.invoke(ListControllerMixin, this);
        this.dataservice = BookService;
        this.books = books;
        this.pk = 'book_id';
        this.fields = [
              {name: 'book_id', pk: true, hide: true}
            , {name: 'name'}
        ];
    }]
);

})();
