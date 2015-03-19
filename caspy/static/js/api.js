(function(){
var mod = angular.module('caspy.api', ['ngResource', 'caspy.server']);

mod.config(['$resourceProvider', 
    function($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }]
);

mod.factory('caspyAPI',
    ['$q', '$http', '$resource', 'Constants',
    function($q, $http, $resource, Constants) {
        var api = {
            root: null

            , resolve: function(name, item) {
                var d = $q.defer();
                if (typeof api.root[name] === 'undefined') {
                    d.reject(new Error(name + ' endpoint not available'));
                }
                else {
                    if (item)
                        d.resolve(api.root[name] + item + '/');
                    else
                        d.resolve(api.root[name]);
                }
                return d.promise;
            }

            , get_endpoint: function(name, item) {
                if (api.root)
                    return api.resolve(name, item);
                return $http.get(Constants.apiRootUrl)
                    .then(function(response) {
                            api.root = response.data;
                            return api.resolve(name, item);
                    })
            }

            , get_resource: function(name) {
                return api.get_endpoint(name)
                        .then(api.build_resource);
            }

            , build_resource: function(endpoint) {
                var d = $q.defer();
                d.resolve($resource(endpoint + ':item/'));
                return d.promise;
            }

        };
        return api;
    }]
);
})();
