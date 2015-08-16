(function(){
var mod = angular.module('caspy.transaction', ['caspy.api', 'caspy.ui', 'generic']);

mod.factory('TransactionService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        function splitcmp(a, b) {
            if (0 < a.amount && 0 < b.amount)
                return 1/a.amount - 1/b.amount;
            return a.amount - b.amount;
        }

        function mapTransactions(transactions) {
            return transactions.map(function(xdata) {
                var xact = {
                    'date': xdata.date,
                    'description': xdata.description,
                    'splits': xdata.splits.sort(splitcmp)
                };
                return xact;
            });
        }

        return function(book_id) {
            var res = caspyAPI.get_resource('transaction', {'book_id': book_id});
            var rw = new ResourceWrapper(res, 'transaction_id');
            rw.orig_all = rw.all;
            rw.all = function() {
                return this.orig_all().then(mapTransactions);
            }
            return rw;
        };
    }]
);

mod.controller('TransactionController'
    ,['$injector'
    , '$routeParams'
    , 'ListControllerMixin'
    , 'TransactionService'
    , function($injector
             , $routeParams
             , ListControllerMixin
             , TransactionService
        ) {
        $injector.invoke(ListControllerMixin, this);
        var ref = this;
        this.book_id = $routeParams['book_id'];
        this.dataservice = TransactionService(this.book_id);
        this.assign('transactions', this.dataservice.all());
        this.pk = 'transaction_id';
    }]
);

mod.controller('TransactionEditController'
    ,['$scope', 'focus',
    function($scope, focus) {
        var ctrl = this;
        this.splits = function(splits) {
            if (arguments.length)
                $scope.transaction.splits = splits;
            return $scope.transaction.splits;
        };
        this.addSplit = function addSplit(amount) {
            console.log('addSplit', amount);
            var splitObj = {
                     'amount': amount
                    ,'status': 'n'
                    ,'number': ''
                    ,'description': ''
                };
            splitObj.auto = true;
            this.splits().push(splitObj);
            if (arguments.length)
                focus('split.auto');
        };
        this.onSplitChange = function(split) {
            split.auto = false;
            var total = 0;
            var auto;
            this.splits().forEach(function(s, i) {
                if (s.auto)
                    auto = s;
                else
                    total += +s.amount;
            });
            if (0 != total) {
                if (auto)
                    auto.amount = -total;
                else
                    this.addSplit(-total);
            }
        };
        this.onTransactionChange = function() {
            if (typeof this.splits() === 'undefined')
                this.splits([]);
            if (0 == this.splits().length)
                this.addSplit();
            focus("cspFocus == 'date'");
        }
        $scope.$watch('transaction', function() {
            if ($scope.transaction)
                ctrl.onTransactionChange();
        });
    }]
);

mod.directive('cspTransactionEdit', function() {
    return {
          scope: {
            transaction: '='
          }
        , controller: 'TransactionEditController'
        , templateUrl: 'partials/transaction/transaction-edit.html'
    };
});

})();
