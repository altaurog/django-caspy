(function(){
var mod = angular.module('caspy.split', []);

mod.controller('SplitController'
    ,['$scope'
    , '$routeParams'
    , 'AccountChoiceService'
    , function($scope, $routeParams, AccountChoiceService) {
        var ref = this;
        this.book_id = $routeParams['book_id'];
        this.accountchoiceservice = AccountChoiceService(this.book_id);
        this.accountchoiceservice.choices.then(function(choices) {
            ref.accountchoices = choices;
        });
        this.accountPath = function() {
            return this.accountchoiceservice.lookup($scope.split.account_id);
        };

        this.credit = function(val) {
            if (arguments.length)
                this.setAmount(-val);
            if ($scope.split.amount < 0)
                return (-$scope.split.amount).toFixed(2);
        };

        this.debit = function(val) {
            if (arguments.length)
                this.setAmount(+val);
            if ($scope.split.amount > 0)
                return (+$scope.split.amount).toFixed(2);
        };

        this.setAmount = function(amount) {
            $scope.split.amount = amount;
            this.transactionctrl.onSplitChange($scope.split);
        }
    }]
);

mod.directive('cspSplit', function() {
    return {
          scope: {'split': '=cspSplit'}
        , controller: 'SplitController'
        , controllerAs: 'splitctrl'
        , transclude: true
        , require: '?^^cspTransactionEdit'
        , link: function(scope, elem, attrs, ctrl, transclude) {
            scope.splitctrl.transactionctrl = ctrl;
            transclude(scope.$new(), function(clone) {
                elem.append(clone);
            });
          }
    }
});

})();

