(function(){
var mod = angular.module('caspy.currency', ['caspy.api', 'generic']);

mod.factory('CurrencyService', ['$q', 'ResourceWrapper', 'caspyAPI',
    function($q, ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('currency');
        var cs = new ResourceWrapper(res, 'cur_code');
        cs.choice = function(currency) {
            return [currency.cur_code, currency.long_name];
        };

        cs.choices = function() {
            var d = $q.defer();
            this.all().then(function(all) {
                all.$promise.then(
                    function(data) { d.resolve(data.map(cs.choice)); },
                    function(message) { d.reject(message); }
                );
            });
            return d.promise;
        }
        return cs;
    }]
);

mod.controller('CurrencyController',
    ['$injector', 'ListControllerMixin', 'CurrencyService', 'currencies',
    function($injector, ListControllerMixin, CurrencyService, currencies) {
        $injector.invoke(ListControllerMixin, this);
        this.dataservice = CurrencyService;
        this.currencies = currencies;
        this.pk = 'cur_code';
        this.fields = [
              {name: 'cur_code', long_name: 'Code', pk: true}
            , {name: 'long_name', long_name: 'Name'}
            , {name: 'symbol'}
            , {name: 'shortcut'}
        ];
    }]
);

})();
