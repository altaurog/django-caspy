(function(){
var mod = angular.module('caspy.choice', ['caspy.api']);

mod.factory('ChoiceService', ['$q',
    function($q) {
        return function(dataservice, makeChoice) {
            var p = dataservice.all().then(function(all) {
                return all.$promise;
            });

            var lookupCache = {};
            var d = p.then(function(data) {
                var choices = data.map(makeChoice);
                // cache values to prevent infinite digest loop
                choices.forEach(function(item) {
                    lookupCache[item[0]] = item[1];
                });
                return choices;
            });

            lookup = function (val) {
                if (typeof lookupCache[val] !== 'undefined')
                    return lookupCache[val];
                return d.then(function(cdata) {
                    return lookupCache[val];
                });
            }

            return {
                  data: p
                , choices: d
                , lookup: lookup
            };
        };
    }]
);

})();
