(function(){
    var app = angular.module('angularJsStub', [ ]);
    var queryUrl;
    app.controller('QueryData', function($scope,$http){
        $http.get("https://riskadvisors.herokuapp.com/queryDb").then(function mySucces(response) {
            $scope.datalist = response.data;
        }, function myError(response){
            $scope.datalist = response.statusText;
        });

    });

})();