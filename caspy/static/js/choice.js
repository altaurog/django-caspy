(function(){
var mod = angular.module('caspy.choice', ['caspy.api']);

function choiceLookup(cdata, lookupVal) {
    for (var i = 0; i < cdata.length; i++) {
        if (cdata[i][0] == lookupVal) {
            return cdata[i][1]
        }
    }
    return undefined;
}

mod.factory('ChoiceService', ['$q',
    function($q) {
        return function(dataservice, makeChoice) {
            var p = dataservice.all().then(function(all) {
                return all.$promise;
            });

            var d = p.then(function(data) {
                return data.map(makeChoice);
            });

            return {
                  data: p
                , choices: d
            };
        };
    }]
);

})();
