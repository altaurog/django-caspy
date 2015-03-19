(function(){
var mod = angular.module('caspy.api', ['ngResource', 'caspy.server']);

mod.config(['$resourceProvider', 
    function($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }]
);

function ResourceWrapper(promise, pk) {
    this.resource = promise;

    this.param = function(id) {
        var p = {}
        p[pk] = id;
        return p;
    }

    this.rc = function (fcn) { return this.resource.then(fcn); }

    this.all = function() {
        return this.rc(function(res) { return res.query(); });
    }

    this.get = function(id) {
        var p = this.param(id)
        return this.rc(function(res) { return res.get(p); });
    }

    this.save = function(obj) {
        return this.rc(function(res) { return res.save(obj); });
    }

    this.del = function(id) {
        var p = this.param(id)
        return this.rc(function(res) { return res.delete(p); });
    }
}

mod.factory('ResourceWrapper', function() { return ResourceWrapper; });

mod.factory('caspyAPI',
    ['$q', '$http', '$resource', 'Constants',
    function($q, $http, $resource, Constants) {
        var api = {
            root: null
            , resources: {}

            , get_resource: function(name) {
                if (typeof api.resources[name] !== 'undefined')
                    return api.resources[name];
                return api.resources[name] = api.get_endpoint(name)
                        .then(api.build_resource);
            }

            , get_endpoint: function(name) {
                if (api.root)
                    return api.resolve(name);
                return $http.get(Constants.apiRootUrl)
                    .then(function(response) {
                            api.root = response.data;
                            return api.resolve(name);
                    })
            }

            , build_resource: function(endpoint) {
                return $resource(endpoint);
            }

            , resolve: function(name) {
                var d = $q.defer();
                if (typeof api.root[name] === 'undefined') {
                    d.reject(new Error(name + ' endpoint not available'));
                }
                else {
                    d.resolve(api.root[name]);
                }
                return d.promise;
            }

        };
        return api;
    }]
);
})();
