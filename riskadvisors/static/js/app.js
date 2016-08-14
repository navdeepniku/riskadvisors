(function(){
    var app = angular.module('angularJsStub', [ ]);
    var querypass = {1:'1',id:'id'};
    app.controller('QueryData', function($scope,$http){
        $http({
            url: '/queryDb',
            method: "POST",
            data: querypass
        }).then(function mySuccess(response) {
            $scope.datalist = response.data;
        }, function myError(response){
            $scope.datalist = response.statusText;
        });

    });

})();