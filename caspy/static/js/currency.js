(function(){
var mod = angular.module('caspy.currency', ['caspy.api']);

mod.factory('CurrencyService', ['ResourceWrapper', 'caspyAPI',
    function(ResourceWrapper, caspyAPI) {
        var res = caspyAPI.get_resource('currency');
        return new ResourceWrapper(res, 'cur_code');
    }]
);

mod.controller('CurrencyController',
    ['$scope', 'CurrencyService', 'currencies',
    function($scope, CurrencyService, currencies) {
        $scope.dataservice = CurrencyService;
        $scope.currencies = currencies;
        $scope.fields = [
              {name: 'cur_code', long_name: 'Code', pk: true}
            , {name: 'long_name', long_name: 'Name'}
            , {name: 'symbol'}
            , {name: 'shortcut'}
        ];
    }]
);

mod.directive('list', function() {
    function isPk(field) {
        return field.pk;
    }
    return {
          templateUrl: 'partials/generic/list.html'
        , scope: {items: '=', fields: '=', restService: '='}
        , compile: function($elem, $attrs) {
            // copy item template url into our own template
            $elem.find('list-item').attr('template', $attrs.itemTemplate);
        }
        , controller: ['$scope', '$route',
            function($scope, $route) {
                var data = $scope.restService;
                var pk = $scope.fields.filter(isPk)[0].name;

                $scope.select = function(item) {
                    $scope.edititem = angular.copy(item);
                    if (item !== null)
                        $scope.edit_code = $scope.edititem[pk];
                    else
                        $scope.edit_code = null;
                };

                $scope.onclose = function() {
                    $scope.select(null);
                };

                $scope.onadd = function(item) {
                    newitem = {};
                    newitem[pk] = '';
                    $scope.select(newitem);
                };

                function save(edit_code, edititem) {
                    if (edit_code)
                        return data.update(edit_code, edititem);
                    return data.create(edititem);
                }

                function reload() {
                    $route.reload();
                }

                $scope.onsave = function() {
                    save($scope.edit_code, $scope.edititem).then(reload);
                }

                function del(edit_code) {
                    return data.del(edit_code)
                }

                $scope.ondel = function() {
                    if ($scope.edit_code)
                        del($scope.edit_code).then(reload);
                }
            }
        ]
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
        return titleCase(field.name);
    return field.long_name;
}

mod.directive('fieldEdit', function() {
    return {
          templateUrl: 'partials/generic/field-edit.html'
        , controller: ['$scope', function($scope) {
            $scope.readonly = false;
            $scope.displayname = displayName($scope.field);
            if ($scope.field.pk === true) {
                $scope.$watch ('edit_code', function(edit_code, _) {
                    $scope.readonly = (edit_code !== '');
                });
            }
        }]
    };
});

})();
