(function(){
var mod = angular.module('caspy.api', ['ngResource', 'caspy.server']);

mod.config(['$resourceProvider', 
    function($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }]
);

function ResourceWrapper(promise, pk) {
    // Provides a little glue
    // ------------------------
    // API endpoints are retrieved in request to API root, which is
    // included in Constants module, in script tag on the base page.
    // This class wraps a promise which carries the $resource object
    // instantiated upon receipt of the endpoint.
    // It also wraps the various api methods and simplifies the calls
    // by constructing the correct arguments when a url containing the
    // object id is necessary.
    // It also extracts and returns the $promise from some of the
    // responses where we normally might want to perform additional
    // actions only after the request is completed, since the $resource 
    // methods return an empty object immediately, which causes
    // funny behavior if we try something like update().then(get()).
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
        var p = this.param(id);
        return this.rc(function(res) { return res.get(p); });
    }

    this.create = function(obj) {
        return this.rc(function(res) { return res.create(obj).$promise; });
    }

    this.update = function(obj_pk, obj) {
        var p = this.param(obj_pk);
        return this.rc(function(res) { return res.update(p, obj).$promise; });
    }

    this.del = function(id) {
        var p = this.param(id);
        return this.rc(function(res) { return res.delete(p).$promise; });
    }
}

mod.factory('ResourceWrapper', function() { return ResourceWrapper; });

mod.factory('caspyAPI',
    ['$q', '$http', '$resource', 'Constants',
    function($q, $http, $resource, Constants) {
        // Load API root endpoints and construct $resource objects
        // necessary for interacting with backend.
        var api = {
            root: null
            , actions: {
                  'create': { method: 'POST' }
                , 'update': { method: 'PUT' }
            }
            , resources: {}

            , get_resource: function(name, params) {
                var ip = params || {};
                function build_res(endpoint) {
                    return api.build_resource(endpoint, ip);
                }
                return api.get_endpoint(name).then(build_res);
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

            , build_resource: function(endpoint, params) {
                return $resource(endpoint, params, api.actions);
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
