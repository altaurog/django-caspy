(function(){
var mod = angular.module('caspy.book', ['caspy.api']);

mod.factory('BookService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('book');
        return new ResourceWrapper(res, 'book_id');
    }]
);

mod.controller('BookController',
    ['$scope', 'BookService', 'books',
    function($scope, BookService, books) {
        $scope.dataservice = BookService;
        $scope.books = books;
        $scope.fields = [
              {name: 'book_id', pk: true, hide: true}
            , {name: 'name'}
        ];
    }]
);

})();
