let map;
let markers = []; // To hold the fixed markers
let marker; // Declare the marker variable
let infoWindows = []; // Declare the infoWindows array

function initMap() {
    var locations = {{ locations|safe }}
  const position1 = { lat: 38.0316, lng: -78.5108 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 16,
    center: position1,
  });

  map.addListener("click", function (mapsMouseEvent) {
    // Get the latitude and longitude from the click event
    const latLng = mapsMouseEvent.latLng;
    const lat = latLng.lat();
    const lng = latLng.lng();

    // Remove the existing marker if one exists
    if (marker) {
      marker.setMap(null);
    }

    // Create a new marker at the clicked position
    marker = new google.maps.Marker({
      position: latLng,
      map: map,
      title: "New Marker",
      icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
    });
    markers.push(marker);

    // Update the form fields
    document.getElementById("latitude").value = lat;
    document.getElementById("longitude").value = lng;
  });

  // Assuming 'locations' is an array defined somewhere in your code
  locations.forEach(function (location) {
    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(location.lat, location.long),
      map: map,
      title: location.name,
      icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
    });

    var contentString =
      '<div id="content">' +
      "<strong>" +
      location.name +
      "</strong><br>" +
      "<strong>" +
      "Likes: " +
      location.likes +
      "</strong><br>" +
      '<a href="' +
      location.url +
      '">Visit Page</a>' +
      "</div>";

    var infowindow = new google.maps.InfoWindow({
      content: contentString,
    });

    infoWindows.push(infowindow);

    marker.addListener("click", function () {
      infoWindows.forEach(function (iw) {
        iw.close();
      });

      infowindow.open(map, marker);
    });

    markers.push(marker);
  });

  const input = document.getElementById("pac-input");
  const searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();

    if (places.length === 0) {
      return;
    }

    // Remove the existing marker if one exists
    if (marker) {
      marker.setMap(null);
    }

    // Create a new marker at the selected place
    marker = new google.maps.Marker({
      map: map,
      title: places[0].name,
      position: places[0].geometry.location,
    });

    const lat = places[0].geometry.location.lat();
    const lng = places[0].geometry.location.lng();

    // Update the form fields
    document.getElementById("latitude").value = lat;
    document.getElementById("longitude").value = lng;

    map.setCenter(places[0].geometry.location);
  });

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const userPos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };
    });
  }
}

initMap();
window.initMap = initMap;
