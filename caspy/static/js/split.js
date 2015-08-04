(function(){
var mod = angular.module('caspy.split', []);

mod.factory('Split', [
    function() {
        var Split = function(splitdata) {
            this.number = splitdata.number;
            this.description = splitdata.description;
            this.account_id = splitdata.account_id;
            this.status = splitdata.status;
            this.amount = splitdata.amount;
        };
        Object.defineProperty(Split.prototype, 'debit', {
            get: function() {
                if (this.amount > 0)
                    return +this.amount;
                return '';
            }
           ,set: function(val) { this.amount = +val; }
        });
        Object.defineProperty(Split.prototype, 'credit', {
            get: function() {
                if (this.amount < 0)
                    return -this.amount;
                return '';
            }
           ,set: function(val) { this.amount = -val; }
        });
        return Split;
    }]
);


})();

