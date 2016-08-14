(function(){
    var app = angular.module('angularJsStub', [ ]);
    var queryUrl;
    app.controller('QueryData', function($scope,$http){
        $http.get('/queryDb').then(function mySucces(response) {
            $scope.datalist = response.data;
        }, function myError(response){
            $scope.datalist = response.statusText;
        });

    });

})();