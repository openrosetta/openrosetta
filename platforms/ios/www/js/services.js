angular.module('pickyourphysician.services', ['ngResource'])

/**
 * A simple example service that returns some data.
 */
.factory('Physicians', ['$resource','$ionicPopup','$state', '$ionicViewService', function($resource, $ionicPopup, $state, $ionicViewService) {
        //alert('entrato');
        var server = "http://api.openrosetta.co.vu";
        return {
            find_all: $resource(server + "/babylon/5377fac415b943000e1a80a3",{
            },{
                query: {
                    method: 'GET',
                    isArray:true,
                    transformResponse: function (data) {
                        //console.log(angular.fromJson(data).data);
                        return angular.fromJson(data).data;
                    }
                }
            })
        };
}]);
