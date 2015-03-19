(function(){
var mod = angular.module('caspy.book', ['caspy.api']);

mod.factory('BookService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('book');
        return new ResourceWrapper(res, 'book_id');
    }]
);

mod.controller('BookController',
    ['$scope', 'books',
    function($scope, books) {
        $scope.books = books;
    }]
);

mod.controller('BookDetailController',
    ['$scope', '$location', 'BookService', 'book',
    function($scope, $location, BookService, book) {
        $scope.book = book;
        $scope.del = function(){
            return BookService.del($scope.book.book_id)
                .then(function() { $location.path('/book/'); });
        };
    }]
);

mod.controller('BookEditController',
    ['$scope', '$location', 'BookService',
    function($scope, $location, BookService) {
        $scope.save = function() {
            return BookService.save($scope.book)
                .then(function() { $location.path('/book/'); });
        };
    }]
);

})();
