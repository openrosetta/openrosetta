angular.module('pickyourphysician.services', ['ngResource'])

/**
 * A simple example service that returns some data.
 */
.factory('Physicians', ['$resource','$ionicPopup','$state', '$ionicViewService', function($resource, $ionicPopup, $state, $ionicViewService) {
        //alert('entrato');
        var server = "http://api.openrosetta.co.vu/homer:8080";
        return {
            register_card: $resource(server + "/cardrequest/api/insert_card_registration",{
                name:'@name',
                surname:'@surname',
                email:'@email'
            },{
                query: {
                    method: 'GET',
                    isArray: true,
                    transformResponse: function (data) {
                        if(angular.fromJson(data).error){
                            $ionicPopup.alert({
                                title: 'Errore',
                                content: angular.fromJson(data).error
                            }).then(function(res) {
                            });
                        }else{

                        }
                        //alert(angular.fromJson(data).user.name)
                        return data;
                    }
                }
            })
        };
}]);
