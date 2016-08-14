(function(){
    var app = angular.module('angularJsStub', [ ]);

    app.controller('QueryData', function($scope,$http){
        $http.get( {{ url_for('queryDb') }} ).then(function mySucces(response) {
            $scope.datalist = response.data;
        }, function myError(response){
            $scope.datalist = response.statusText;
        });

    });

})();