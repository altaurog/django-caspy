(function(){
var mod = angular.module('caspy.transaction', ['caspy.api', 'caspy.split', 'generic', 'MassAutoComplete']);

mod.factory('TransactionService', ['Split', 'ResourceWrapper', 'caspyAPI',
    function(Split, ResourceWrapper, caspyAPI) {
        function mapSplits(sdata) {
            return sdata.map(function(splitdata) { return new Split(splitdata); });
        }

        function mapTransactions(transactions) {
            return transactions.map(function(xdata) {
                var xact = {
                    'date': xdata.date,
                    'description': xdata.description,
                    'splits': mapSplits(xdata.splits)
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
    , 'AccountChoiceService'
    , function($injector
             , $routeParams
             , ListControllerMixin
             , TransactionService
             , AccountChoiceService
        ) {
        $injector.invoke(ListControllerMixin, this);
        var ref = this;
        this.book_id = $routeParams['book_id'];
        this.dataservice = TransactionService(this.book_id);
        this.assign('transactions', this.dataservice.all());
        this.pk = 'transaction_id';
        this.accountchoiceservice = AccountChoiceService(this.book_id);
        this.accountlookup = this.accountchoiceservice.lookup;
    }]
);

})();
