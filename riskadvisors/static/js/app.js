(function(){
    var app = angular.module('angularJsStub', [ ]);
    app.controller('QueryData', function($scope,$http){
        $http({
            url: '/queryDb',
            method: "POST",
            headers: { ' Content-Type': 'application/json'},
            data: JSON.stringify(querypass)
        }).success(function(data)){
            $scope.datalist = data;
        }
    
        });

})();