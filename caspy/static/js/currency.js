(function(){
var mod = angular.module('caspy.currency', ['caspy.api', 'caspy.choice', 'generic']);

mod.factory('CurrencyService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('currency');
        return new ResourceWrapper(res, 'cur_code');
    }]
);

mod.factory('CurrencyChoiceService', ['ChoiceService', 'CurrencyService',
    function(ChoiceService, CurrencyService) {
        function makeChoice(currency) {
            return [currency.cur_code, currency.long_name];
        };
        return ChoiceService(CurrencyService, makeChoice);
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
