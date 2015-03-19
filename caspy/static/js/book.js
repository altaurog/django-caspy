(function(){
var mod = angular.module('caspy.book', ['caspy.api']);

mod.factory('BookService', ['$q', 'caspyAPI',
    function($q, caspyAPI) {
        var cs;
        var res = caspyAPI.get_resource('book');
        function rc(fcn) { return res.then(fcn); }
        return cs = {
              all: function() {
                return rc(function(res) { return res.query(); });
                }
            , get: function(id) {
                return rc(function(res) { return res.get({id: id}); });
                }
            , save: function(book) {
                return rc(function(res) { return res.save(book); });
                }
            , del: function(id) {
                return rc(function(res) { return res.delete({id: id}); });
                }
            };
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
