// Library for application-wide animation
angular.module('Animation_Library', ['ngAnimate'])
.controller('Sidebar', ['$scope', function($scope) {
    $scope.getState = () => ($scope.hovered == null) ? {'open': false} :
                            ($scope.hovered == false) ? {'closed': true} : 
                            {'open': true};
}]);





