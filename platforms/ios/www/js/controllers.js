angular.module('pickyourphysician.controllers', ['pickyourphysician.services'])

    .controller('MainCtrl', function($scope, $ionicSideMenuDelegate) {
    })

    .controller('HomeCtrl', function($scope, $ionicSideMenuDelegate) {
    })

    .controller('MapCtrl', function($scope, $ionicLoading, $ionicSideMenuDelegate, $ionicActionSheet, Physicians) {
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
                zoom: 7,
                mapTypeId: google.maps.MapTypeId.ROADMAP,

            };
            var map = new google.maps.Map(document.getElementById("map"),
                mapOptions);

            // Stop the side bar from dragging when mousedown/tapdown on the map
            google.maps.event.addDomListener(document.getElementById('map'), 'mousedown', function(e) {
                e.preventDefault();
                return false;
            });

            var addresses = Physicians.find_all.query();
            var geocodablePh = [];

            var geocodePhs = function(idx){
                if (geocodablePh.length <= idx) {
                    console.log(idx, geocodablePh.length);
                    return;
                }
                var ph = geocodablePh[idx];
                geocoder.geocode( { 'address': ph.INDIRIZZO_AMB}, function(results, status) {

                    if (status == google.maps.GeocoderStatus.OK) {
                        //map.setCenter(results[0].geometry.location);
                        //var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
                        console.log('aggiunto');
                        var marker = new google.maps.Marker({
                            map: map,
                            draggable:true,
                            animation: google.maps.Animation.DROP,
                            position: results[0].geometry.location,
                            address: ph.INDIRIZZO_AMB,
                            number: ph.TELEFONO_PRIMARIO_AMB,
                            icon: 'http://mypins.com/images/redcross.gif'
                        });

                        var html =
                            ph.TELEFONO_PRIMARIO_AMB+" "+ph.INDIRIZZO_AMB;

                        var infowindow = new google.maps.InfoWindow({
                            content: html
                        });
                        google.maps.event.addListener(marker, 'click', function(){
                            console.log(marker);
                            //infowindow.open(map, marker)
                            $scope.show(marker.address,marker.number);
                        });
                        //$scope.myMarkers.push(marker);
                        setTimeout(function() { geocodePhs(idx+1); }, 200);

                    } else if (status == google.maps.GeocoderStatus.OVER_QUERY_LIMIT){
                        setTimeout(function() { geocodePhs(idx); }, 400);
                    } else {
                        geocodePhs(idx+1);
                    }
                });
            };
            addresses.$promise.then(function(addresses){

                angular.forEach(addresses, function(x) {
                    angular.forEach(x, function(y){
                        geocodablePh.push(y);
                    });
                });
                geocodePhs(0);
            });

            $scope.codeAddress = function(){

                var address = document.getElementById("address").value;
                geocoder.geocode( { 'address': address}, function(results, status) {

                    if (status == google.maps.GeocoderStatus.OK) {
                        map.setCenter(results[0].geometry.location);
                        map.setZoom(12);
                    } else {
                        //alert("Indirizzo non trovato: " + status);
                        //alert("Indirizzo non trovato!");
                    }
                });

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
                            window.open("comgooglemaps://?saddr=&daddr="+address+"&directionsmode=driving");
                    }
                    return true;
                }

            });
        };
    });
