import Ajax from './Ajax.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());

const mapsFunction = function () {
	
	if (window.google) {
		var map;
		var myOptions = {
			zoom: 6.9,
			center: new google.maps.LatLng(37.984377, 23.7260427), //put Athens in the middle
			scrollwheel: false, //disable mouse scroll wheel scaling
			mapTypeId: 'satellite'
        };

        map = new google.maps.Map($('#map_canvas')[0], myOptions);

        var table=$('#ts_table').DataTable({
            paging: false
        });
        
        //var infowindow = new google.maps.InfoWindow();

		function addMarker(name, coordinate, map) {

            var marker = new google.maps.Marker({
				position: coordinate,
                map: map,   
                title: name,
            });
            
            google.maps.event.addListener(marker, 'click', function (e) {
                
                const url = HomeRoutes.home.latest_ts + marker.title+'/';
                ajax.get(url, {}).then((return_data) => {
                    
                    const title= return_data.info.platform+" ("+return_data.info.lat+", "+return_data.info.lon+") <br/>" +return_data.info.date;
                    $('#mapModalLabel').html(title);
                    const param_list=Object.keys(return_data.params);
                    
                    
                    var i=0;
                    for (var p in return_data.params) {
                        for (var d in return_data.params[p]){
                            var elem =return_data.params[p][d];
                            table.row.add(
                                  [elem['description'],d,elem['val'],elem['valqc']],
                            )
                        }
                    }
                    
                    table.order.fixed( {
                        pre: [[ 0, 'asc' ]]
                    } );
                    table.draw();
                    
                    }).catch((error) => {
                    const err = new AjaxError(error);
                    console.log(err);
                    });
                $('#mapModal').modal('show');
               
			});

        }

        ajax.get(HomeRoutes.home.map, {}).then((return_data) => {
        
            for (var x = 0; x <return_data.count; x++) {
                const latlng = new google.maps.LatLng(return_data.results[x].lat, return_data.results[x].lon);
                const name=return_data.results[x].tspr+'_'+return_data.results[x].type+'_'+return_data.results[x].pid;
                addMarker(name, latlng, map);
            }
          }).catch((error) => {
            const err = new AjaxError(error);
            console.log(err);
          });
        
			
    }
};

export {
    mapsFunction
};