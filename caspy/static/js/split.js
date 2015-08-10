(function(){
var mod = angular.module('caspy.split', []);

mod.controller('SplitController'
    ,['$routeParams'
    , 'AccountChoiceService'
    , function($routeParams, AccountChoiceService) {
        this.book_id = $routeParams['book_id'];
        this.accountchoiceservice = AccountChoiceService(this.book_id);
        this.accountPath = function() {
            return this.accountchoiceservice.lookup(this.split.account_id);
        };

        this.credit = function() {
            if (this.split.amount < 0)
                return (-this.split.amount).toFixed(2);
        };

        this.debit = function() {
            if (this.split.amount > 0)
                return (+this.split.amount).toFixed(2);
        };
    }]
);

mod.directive('cspSplit', function() {
    return {
          scope: {'split': '=cspSplit'}
        , controller: 'SplitController'
        , bindToController: true
        , controllerAs: 'ctrl'
        , transclude: true
        , link: function(scope, elem, attrs, ctrl, transclude) {
            transclude(scope.$new(), function(clone) {
                elem.append(clone);
            });
          }
    }
});

})();

