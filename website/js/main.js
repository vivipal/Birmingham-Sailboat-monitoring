function async_show_position(map,layerGroup){

  var boat_icon = L.icon({ iconUrl: 'img/boat.png',
                           iconSize:     [26, 70], // size of the icon
                           iconAnchor:   [13, 35], // point of the icon which will correspond to marker's location
                           popupAnchor:  [13, -10] // point from which the popup should open relative to the iconAnchor
                           });


  $.getJSON('get_position.php',function(jsonData) {
    boat_data = jsonData

    var history_coord = history_line.getLatLngs();
    if (history_coord.length > 0){
      if (Math.abs(history_coord[history_coord.length-1].lat - boat_data[0]['lat']) > 0.000001 || Math.abs(history_coord[history_coord.length-1].lon - boat_data[0]['lon']) > 0.000001) {
        history_line.addLatLng({lon: boat_data[0]['lon'], lat: boat_data[0]['lat']});
      }
    }else{
      history_line.addLatLng({lon: boat_data[0]['lon'], lat: boat_data[0]['lat']});
    }

    layerGroup.clearLayers();
    L.marker({lon: boat_data[0]['lon'], lat: boat_data[0]['lat']},{rotationAngle: boat_data[0]['heading'],icon: boat_icon}).addTo(layerGroup);
    var arrowOptions_HEADING = {distanceUnit: 'px',
                                isWindDegree: true,
                                stretchFactor: -1,
                                color: '#2F2',
                                opacity: 0.7,
                                weight: 6,
                                arrowheadLength:20};

    var arrowData_HEADING = {latlng: L.latLng(boat_data[0]['lat'], boat_data[0]['lon']),
                             degree: boat_data[0]['heading'],
                             distance: 75,
                             title: "heading"};
    var arrow_HEADING = new L.Arrow(arrowData_HEADING, arrowOptions_HEADING);
    arrow_HEADING.addTo(layerGroup);

    var arrowOptions_TW = {distanceUnit: 'px',
                           isWindDegree: true,
                           stretchFactor: -1,
                           reverse: true,
                           offset:50,
                           color: '#00F',
                           opacity: 1,
                           weight: 6,
                           arrowheadLength:20};
    var arrowData_TW = {latlng: L.latLng(boat_data[0]['lat'], boat_data[0]['lon']),
                        degree: boat_data[0]['true_wind_direction'],
                        distance: 100,
                        title: "True wind direction"};
    var arrow_TW = new L.Arrow(arrowData_TW, arrowOptions_TW);
    arrow_TW.addTo(layerGroup);
  });
}

function async_show_wps(map,layerGroup){

    $.getJSON('get_wps.php',function(jsonData) {
      line_data = jsonData
      layerGroup.clearLayers();
      for (i=0; i<line_data.length-1;i++)	{
          var latlngs = [[line_data[i]['lat'], line_data[i]['lon']],
                         [line_data[i+1]['lat'], line_data[i+1]['lon']]];
          var polyline = L.polyline(latlngs, {color: 'red',opacity: 0.8});
          polyline.addTo(layerGroup);
          L.marker({lon: line_data[i]['lon'], lat: line_data[i]['lat']}).bindPopup("wp n°"+(i+1)).addTo(layerGroup);
        }
        L.marker({lon: line_data[line_data.length-1]['lon'], lat: line_data[line_data.length-1]['lat']}).bindPopup("wp n°"+line_data.length).addTo(layerGroup);
    });
}
