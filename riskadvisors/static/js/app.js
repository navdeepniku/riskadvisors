(function(){
    var app = angular.module('angularJsStub', [ ]);
    var querypass = {col_value:'1',col_name:'id'};
    app.controller('QueryData',function($scope,$http){

        $scope.query = function ($qdata) {
            $http({
            url: '/queryDb',
            method: "POST",
            data: qdata
        }).then(function mySuccess(response) {
            $scope.datalist = response.data;
        }, function myError(response){
            $scope.datalist = response.statusText;
        });
        }

        });

})();