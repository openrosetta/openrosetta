angular.module('pickyourphysician.controllers', ['pickyourphysician.services'])

    .controller('MainCtrl', function($scope, $ionicSideMenuDelegate) {
    })

    .controller('HomeCtrl', function($scope, $ionicSideMenuDelegate) {
    })

    .controller('MapCtrl', function($scope, $ionicLoading, $ionicSideMenuDelegate, $ionicActionSheet) {
        var geocoder;
        if (!$scope.myMarkers) {
            $scope.myMarkers = [];
        }
        setTimeout(function(){
            initialize();
        },1000);
        function initialize() {
            geocoder = new google.maps.Geocoder();
            var mapOptions = {
                center: new google.maps.LatLng(45.070312,7.686856),
                zoom: 12,
                mapTypeId: google.maps.MapTypeId.ROADMAP,

            };
            var map = new google.maps.Map(document.getElementById("map"),
                mapOptions);

            // Stop the side bar from dragging when mousedown/tapdown on the map
            google.maps.event.addDomListener(document.getElementById('map'), 'mousedown', function(e) {
                e.preventDefault();
                return false;
            });


            $scope.codeAddress = function(){
                angular.forEach($scope.myMarkers, function(marker) {
                    marker.setMap(null);
                });
                var address = document.getElementById("address").value;
                var addresses = ['Corso San Maurizio 19 Torino', 'Corso Francia 101 Torino', 'Corso Vittorio Torino'];
                var numbers = ['0119284727', '08124948723', '0118395734'];
                var addr = addresses.length;

                while(addr--){
                    (function(addr){
                        geocoder.geocode( { 'address': addresses[addr]}, function(results, status) {
                            var addr_id = addr;
                            console.log(addr_id);
                            console.log(addresses);
                            if (status == google.maps.GeocoderStatus.OK) {
                                map.setCenter(results[0].geometry.location);
                                //var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
                                var marker = new google.maps.Marker({
                                    map: map,
                                    draggable:true,
                                    animation: google.maps.Animation.DROP,
                                    position: results[0].geometry.location,
                                    address:addresses[addr_id],
                                    number:numbers[addr_id],
                                    icon: 'http://mypins.com/images/redcross.gif'
                                });
                                
                                var html =
                                    numbers[addr_id]+" "+addresses[addr_id];

                                var infowindow = new google.maps.InfoWindow({
                                    content: html
                                });
                                google.maps.event.addListener(marker, 'click', function(){
                                    console.log(marker);
                                    //infowindow.open(map, marker)
                                    $scope.show(marker.address,marker.number);
                                });
                                $scope.myMarkers.push(marker);

                            } else {
                                //alert("Indirizzo non trovato: " + status);
                                alert("Indirizzo non trovato!");
                            }
                        });
                    })(addr);
                }
            }

            $scope.map = map;
        }
        //google.maps.event.addDomListener(window, 'load', initialize);

        $scope.show = function(address,number) {

            // Show the action sheet
            $ionicActionSheet.show({
                titleText: 'Medico: ' + address + ", " + number,
                buttons: [
                    { text: 'Chiama' },
                    { text: 'Arriva' }
                ],

                cancelText: 'Cancel',
                cancel: function() {
                    console.log('CANCELLED');
                },
                buttonClicked: function(index) {
                    console.log('BUTTON CLICKED', index);
                    if(index==0){
                        window.open("tel:"+ number,'_top');
                    }
                    if(index==1){
                        if(ionic.Platform.isAndroid())
                            window.open("http://maps.google.com/maps?saddr=&daddr="+address+"&directionsmode=driving");
                        if(ionic.Platform.isIOS())
                            window.open("comgooglemaps://?saddr=Current Location&daddr="+address+"&directionsmode=driving");
                    }
                    return true;
                }

            });
        };
    });
