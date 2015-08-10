(function(){
var mod = angular.module('generic', []);

mod.factory('ListControllerMixin', ['$q', function($q) {
    function mixin($route) {
        this.select = function(item) {
            this.edititem = angular.copy(item);
            if (item !== null)
                this.edit_code = this.edititem[this.pk];
            else
                this.edit_code = null;
        };

        this.close = function() {
            this.select(null);
        };

        this.add = function(item) {
            newitem = {};
            newitem[this.pk] = '';
            this.select(newitem);
        };

        this._save = function(edit_code, edititem) {
            if (edit_code)
                return this.dataservice.update(edit_code, edititem);
            return this.dataservice.create(edititem);
        };

        this.reload = function() {
            $route.reload();
        };

        this.save = function() {
            this._save(this.edit_code, this.edititem).then(this.reload);
        };

        this._del = function(edit_code) {
            return this.dataservice.del(edit_code)
        };

        this.del = function() {
            if (this.edit_code)
                this._del(this.edit_code).then(this.reload);
        };

        this.fieldvisible = function(field) {
            return !field.hide;
        };

        this.assign = function (name, promise) {
            var ref = this;
            promise.then(function(data) { ref[name] = data; });
        };

        this.choiceFields = function(cflist) {
            var ref = this;
            var promises = cflist.map(function(cf) {
                var i = cf[0];
                var name = cf[1];
                var promise = cf[2];
                var empty = cf[3];
                return promise.then(function(data) {
                    if (typeof empty !== 'undefined')
                        data.unshift(empty);
                    ref.fields.push({i: i, name: name, choices: data});
                });
            });
            $q.all(promises).then(function() { ref.sortFields(); });
        };

        this.fieldCompare = function(a, b) { return a.i - b.i; };

        this.sortFields = function() {
            this.fields.sort(this.fieldCompare);
        };
    }
    mixin.$inject = ['$route'];
    return mixin;
}]);

function capFirst(word) {
    return word.charAt(0).toUpperCase() + word.substr(1).toLowerCase();
}

function titleCase(str) {
    return str.replace(/\w\S*/g, capFirst);
}

function displayName(field) {
    if ('undefined' === typeof field.long_name)
        return titleCase(field.name.replace('_', ' '));
    return field.long_name;
}

mod.directive('fieldEdit', function() {
    return {
          templateUrl: 'partials/generic/field.html'
        , controller: ['$scope', function($scope) {
            $scope.readonly = '';
            if ($scope.field.choices)
                $scope.display = 'select';
            $scope.displayname = displayName($scope.field);
            if ($scope.field.pk === true) {
                $scope.$watch ('listcontroller.edit_code', function(edit_code, _) {
                    if ($scope.readonly = edit_code)
                        $scope.display = 'readonly';
                });
            }
        }]
    };
});

})();
