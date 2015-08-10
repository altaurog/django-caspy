(function(){
var mod = angular.module('caspy.transaction', ['caspy.api', 'generic']);

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

})();
