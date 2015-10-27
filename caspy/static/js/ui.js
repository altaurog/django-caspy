(function(){
var mod = angular.module('caspy.ui', []);

/* http://stackoverflow.com/a/18295416/519015 */

// Focus first input element when broadcast expression evaluates true
mod.directive('cspFocus', function() {
    return {
        link: function(scope, elem, attr) {
            scope.$on('cspfocus', function(e, test) {
                if (scope.$eval(test, {cspFocus: attr.cspFocus})) {
                    var input = findInput(elem);
                    if (input)
                        input.select();
                }
            });
        }
    };
});

function findInput(elem) {
    if (elem[0].tagName == 'INPUT')
        return elem[0];
    return elem.find('input').eq(0)[0];
}

mod.factory('focus', ['$rootScope', '$timeout',
    function($rootScope, $timeout) {
        return function(func) {
            $timeout(function() {
                $rootScope.$broadcast('cspfocus', func);
            });
        };
    }]
);

mod.factory('scroll', function() {
    return function(offset) {
        var webkit = document.body, ffie = document.documentElement;
        if (arguments.length) {
            ffie.scrollTop = webkit.scrollTop = offset;
        }
        return ffie.scrollTop || webkit.scrollTop;
    };
});

})();
