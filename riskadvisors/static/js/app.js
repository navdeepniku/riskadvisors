(function(){
    var app = angular.module('angularJsStub', [ ]);

    var phone={ram: '512', cpu: 1};
    app.controller('PhoneSpecs', function(){
        this.device = phone;
    })

})();