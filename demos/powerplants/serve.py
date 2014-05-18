import types
from xml2dict import xmlreader
from dbf import dbfreader
from csv import DictReader, Sniffer


def load_data():
    data = []

    import os
    for entry in os.listdir('data'):
        path = os.path.join('data', entry)
        if entry.endswith('dbf'):
            d = dbfreader(open(path))
        elif entry.endswith('csv'):
            f = open(path)
            dialect = Sniffer().sniff(f.read(1024), delimiters=';,')
            f.seek(0)
            d = DictReader(f, dialect=dialect)
        else:
            d = xmlreader(open(path))
        data.append(d)

    return data


from wsgiref.simple_server import make_server
from tg import expose, TGController, AppConfig

class RootController(TGController):
    @expose()
    def index(self):
        return '''
<html>
    <head>
        <style>
            #map-canvas {
                width: 100%;
                height: 100%;
            }
        </style>
        <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
        <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD2r5wGO8TiV5VhEQzVMm8dfGIHaaOC3Kg&sensor=false"></script>
        <script type="text/javascript">
          function put_marker(map, location, name, power) {
               var marker = new google.maps.Marker({
                    map:map,
                    draggable:true,
                    animation:google.maps.Animation.DROP,
                    position:location
                });
                var html = "" + name + " :: " + power + "MW";
                var infoWindow = new google.maps.InfoWindow({
                    content:html
                });
                google.maps.event.addListener(marker,'click', function(){
                    infoWindow.open(map,marker);
                }); 
          }

          function initialize() {
            var mapOptions = {
              center: new google.maps.LatLng(45.0718969, 7.6857533),
              zoom: 6
            };
            var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
            var geocoder = new google.maps.Geocoder();

            $.getJSON('/data', function(data) {
                var data = data.data;
                var counter = 0;
                for (var i=0; i<data.length; i++) {
                    var entry = data[i];
                    var location = entry['position'];
                    if (!location)
                        location = entry['location'];

                    var name = entry['location'];
                    var power = entry['power'];
                    if(!entry['position']) {
                        counter += 1;
                        (function(i, map, location, name, power){
                            setTimeout(function() {
                                geocoder.geocode({'address':location}, function(result, status){
                                    console.log(status);
                                    if(status==google.maps.GeocoderStatus.OK) {
                                        put_marker(map, result[0].geometry.location, name, power);
                                    }
                                });
                            }, i*400);
                        })(counter, map, location, name, power);
                    }
                    else {
                        put_marker(map, new google.maps.LatLng(location[1], location[0]), name, power);
                    }
                }
            });
          }
          google.maps.event.addDomListener(window, 'load', initialize);
        </script>
    </head>
    <body>
      <div id="map-canvas"/>
    </body>
</html>
'''

    @expose('json')
    def data(self):
        data = load_data()
        filtered_data = []

        for entry in data:
            if isinstance(entry, list):
                for row in entry:
                    if 'NOMBRE' in row and 'POTENCIA' in row:
                        filtered_data.append({'location': row['NOMBRE'], 'power': row['POTENCIA'].split()[0].replace(',', '.'), 'position': None})
            elif isinstance(entry, dict):
                entry = entry['kml']['Document']['Folder']['Placemark']
                for row in entry:
                    position = [float(v) for v in row['Point']['coordinates'].split(',')]
                    row = row['ExtendedData']['SchemaData']['SimpleData']
                    rowdict = {}
                    for kvinfo in row:
                        rowdict[kvinfo['@name']] = kvinfo['#text']
                    filtered_data.append({'location': rowdict['Indirizzo'], 'power': float(rowdict['PotenzakW'])/1000, 'position': position})
            else:
                for row in entry:
                    total_power = 0
                    if row['POTENZA_da_116_a_350_KW']:
                        total_power += int(row['POTENZA_da_116_a_350_KW']) * ((116+350)/2.0)

                    if row['POTENZA_da_35_a_116_KW']:
                        total_power += int(row['POTENZA_da_35_a_116_KW']) * ((35+116)/2.0) 

                    if row['POTENZA_uguale_350_KW_e_maggiore']:
                        total_power += int(row['POTENZA_uguale_350_KW_e_maggiore']) * 350.0

                    if total_power:
                        filtered_data.append({'location': row['toponimo'].lower(), 'power': total_power/1000, 'position': None})
            
        return dict(data=filtered_data)


config = AppConfig(minimal=True, root_controller=RootController())
config.renderers = ['json']

print "Serving on port 8080..."
httpd = make_server('', 8080, config.make_wsgi_app())
httpd.serve_forever()

