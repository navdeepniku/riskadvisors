(function(){
    var app = angular.module('angularJsStub', [ ]);
    var querypass = {col_value:'1',col_name:'id'};
    app.controller('QueryData',function($scope,$http){
        $scope.query = function () {
            
            $http({
            url: '/queryDb',
            method: "POST",
            data: {col_name: $scope.col_name, col_value: $scope.col_value}
        }).then(function mySuccess(response) {
            $scope.datalist = response.data;
        }, function myError(response){
            $scope.datalist = response.statusText;
        });
        }

        });

})();