(function(){
var mod = angular.module('caspy.api', ['caspy.server']);

mod.factory('caspyAPI',
    ['$q', '$http', 'Constants', function($q, $http, Constants) {
        var api = {
            root: null,

            resolve: function(name) {
                var d = $q.defer();
                if (typeof api.root[name] === 'undefined')
                    d.reject(new Error(name + ' endpoint not available'));
                else
                    d.resolve(api.root[name]);
                return d.promise;
            },

            get_endpoint: function(name) {
                if (api.root)
                    return api.resolve(name);
                return $http.get(Constants.apiRootUrl)
                    .then(function(response) {
                            api.root = response.data;
                            return api.resolve(name);
                    })
            }
        };
        return api;
    }]
);
})();
