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
