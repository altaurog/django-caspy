(function(){
var mod = angular.module('caspy.transaction', ['caspy.api', 'caspy.ui', 'generic']);

mod.factory('TransactionService', ['ResourceWrapper', 'caspyAPI', 'dateFilter',
    function(ResourceWrapper, caspyAPI, dateFilter) {
        function splitcmp(a, b) {
            if (0 < a.amount && 0 < b.amount)
                return 1/a.amount - 1/b.amount;
            return a.amount - b.amount;
        }

        function deserialize(xdata) {
            return {
                'date': new Date(xdata.date),
                'description': xdata.description,
                'splits': xdata.splits.sort(splitcmp)
            };
        }

        function serialize(xact) {
            return {
                'date': dateFilter(xact.date, 'yyyy-MM-dd'),
                'description': xact.description,
                'splits': xact.splits
            };
        }

        function mapTransactions(transactions) {
            return transactions.map(deserialize);
        }

        return function(book_id) {
            var res = caspyAPI.get_resource('transaction', {'book_id': book_id});
            return new ResourceWrapper(res, 'transaction_id', serialize, deserialize);
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
        this.newitem = function() { return {splits: []}; };
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

        function nonzero(split) {
            return split.amount || split.auto;
        }

        this.onSplitChange = function(split) {
            split.auto = false;
            var total = 0;
            var auto;
            var splits = this.splits(this.splits().filter(nonzero));
            splits.forEach(function(s, i) {
                if (s.auto)
                    auto = i;
                else
                    total += +s.amount;
            });
            if (Math.abs(total) >= 0.1) {
                if (typeof auto !== 'undefined')
                    splits[auto].amount = -total;
                else
                    this.addSplit(-total);
            } else {
                splits.splice(auto, 1);
            }
        };
        this.onTransactionChange = function() {
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
