(function(){
var mod = angular.module('generic', []);

mod.controller('GenericListController', ['$route',
    function($route) {
        var data = this.restService;
        var pk = this.fields.filter(function(f) { return f.pk; })[0].name;

        this.select = function(item) {
            this.edititem = angular.copy(item);
            if (item !== null)
                this.edit_code = this.edititem[pk];
            else
                this.edit_code = null;
        };

        this.close = function() {
            this.select(null);
        };

        this.add = function(item) {
            newitem = {};
            newitem[pk] = '';
            this.select(newitem);
        };

        function _save(edit_code, edititem) {
            if (edit_code)
                return data.update(edit_code, edititem);
            return data.create(edititem);
        }

        function reload() {
            $route.reload();
        }

        this.save = function() {
            _save(this.edit_code, this.edititem).then(reload);
        }

        function _del(edit_code) {
            return data.del(edit_code)
        }

        this.del = function() {
            if (this.edit_code)
                _del(this.edit_code).then(reload);
        }

        this.fieldvisible = function(field) {
            return !field.hide;
        }
    }]
);

mod.directive('list', function() {
    return {
          templateUrl: 'partials/generic/list.html'
        , scope: {items: '=', fields: '=', restService: '='}
        , compile: function($elem, $attrs) {
            // copy item template url into our own template
            $elem.find('list-item').attr('template', $attrs.itemTemplate);
        }
        , controller: 'GenericListController'
        , controllerAs: 'listcontroller'
        , bindToController: true
    };
});

mod.directive('listItem', function() {
    return {
          scope: { item: '=' }
        , templateUrl: function(_, $attrs) { return $attrs.template; }
    };
});

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
            $scope.displayname = displayName($scope.field);
            if ($scope.field.pk === true) {
                $scope.$watch ('listcontroller.edit_code', function(edit_code, _) {
                    $scope.readonly = edit_code;
                });
            }
        }]
    };
});

})();
