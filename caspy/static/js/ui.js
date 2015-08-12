(function(){
var mod = angular.module('caspy.ui', []);

/* http://stackoverflow.com/a/18295416/519015 */
mod.directive('cspFocus', function() {
    return {
        link: function(scope, elem, attr) {
            scope.$on('cspfocus', function(e, test) {
                if (scope.$eval(test, {cspFocus: attr.cspFocus}))
                    elem[0].select();
            });
        }
    };
});

mod.factory('focus', ['$rootScope', '$timeout',
    function($rootScope, $timeout) {
        return function(func) {
            $timeout(function() {
                $rootScope.$broadcast('cspfocus', func);
            });
        };
    }]
);

})();
