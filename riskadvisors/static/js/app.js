(function(){
    var app = angular.module('angularJsStub', [ ]);

    var phone={ram: '512', cpu: 1};
    app.controller('QueryData', function($scope,$http){
        var done=function(resp){
            $scope.lists=respdata;
        };
        var fail=function(err){
            
        };
        $http.get( {{ url_for('queryDb') }} )
        .then(done,fail)
    });

})();