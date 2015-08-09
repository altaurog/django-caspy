(function(){
var mod = angular.module('caspy.choice', []);

mod.factory('ChoiceService', [
    function() {
        return function(dataservice, makeChoice) {
            var p = dataservice.all();

            var res = {
                  data: p
                , choices: p.then(function(d) {
                    var choices = d.map(makeChoice);
                    // cache values to prevent infinite digest loop
                    res.lookupCache = {};
                    choices.forEach(function(item) {
                        res.lookupCache[item[0]] = item[1];
                    });
                    return choices;
                })

                , lookup: function(val) {
                    if (typeof res.lookupCache !== 'undefined')
                        return res.lookupCache[val];
                    return res.choices.then(function(cdata) {
                        return res.lookupCache[val];
                    });
                }
            };
            return res;
        };
    }]
);

})();
