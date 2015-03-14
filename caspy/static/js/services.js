var caspyApp = angular.module('caspyApp');

caspyApp.factory('caspyAPI',
    ['$http', function($http) {
        var api = {
            root: null,

            resolve: function(name, cb) {
                cb(api.root[name]);
            },

            endpoint: function(name, cb) {
                if (api.root)
                    api.resolve(name, cb);
                else
                    $http.get(apiRootUrl).success(function(data) {
                        api.root = data;
                        api.resolve(name, cb);
                    });
            }
        };
        return api;
    }]
);

