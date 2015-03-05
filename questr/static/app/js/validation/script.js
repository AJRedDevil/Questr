// create angular app
	var validationApp = angular.module('validationApp', []);

	// create angular controller
	validationApp.controller('mainController', function($scope) {
		
	});
	
	validationApp.directive('match', function () {
        return {
            require: 'ngModel',
            restrict: 'A',
            scope: {
                match: '='
            },
            link: function(scope, elem, attrs, ctrl) {
                scope.$watch(function() {
                    return (ctrl.$pristine && angular.isUndefined(ctrl.$modelValue)) || scope.match === ctrl.$modelValue;
                }, function(currentValue) {
                    ctrl.$setValidity('match', currentValue);
                });
            }
        };
    });


var postApp = angular.module('postApp', []);
  
postApp.controller('mainController', ['$scope', function($scope) {
	$scope.master = {};
	
	$scope.update = function(user) {
      $scope.master = angular.copy(user);
    };

	
	$scope.reset = function() {
	  $scope.user = angular.copy($scope.master);
	};
	
	$scope.isUnchanged = function(user) {
		
	  return angular.equals(user, $scope.master);
	};
	
	$scope.reset();
}]);








