(function(){
var mod = angular.module('caspy.api', ['caspy.server']);

mod.factory('caspyAPI',
    ['$http', 'Constants', function($http, Constants) {
        var api = {
            root: null,

            resolve: function(name, cb) {
                cb(api.root[name]);
            },

            endpoint: function(name, cb) {
                if (api.root)
                    api.resolve(name, cb);
                else
                    $http.get(Constants.apiRootUrl).success(function(data) {
                        api.root = data;
                        api.resolve(name, cb);
                    });
            }
        };
        return api;
    }]
);
})();
