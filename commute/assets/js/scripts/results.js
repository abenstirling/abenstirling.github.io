/*
Display the results as a pie chart of the commute times
Requires: Charts.js (www.chartjs.org)
          JQuery (www.jquery.com)
*/


/**
 * 
 * @param {*} rawTravelTimes An array of estimated travel times in minutes.
 * @returns A dictionary of times grouped every 10 minutes
 */
function processRawTimes(rawTravelTimes) {
    var timeDict = {
        "<10": 0,
        "10-20": 0,
        "20-30": 0,
        "30-40": 0,
        ">40": 0,
    }
    for (time of rawTravelTimes) {
        if (time < 10) {
            timeDict["<10"] += 1;
        } else if (time >= 10 && time < 20) {
            timeDict["10-20"] += 1;
        } else if (time >= 20 && time < 30) {
            timeDict["20-30"] += 1
        } else if (time >= 30 && time < 40) {
            timeDict["30-40"] += 1
        } else if (time >= 40) {
            timeDict[">40"] += 1
        }
    }

    return timeDict;
}

/**
 * Display the travel times as a pie chart.
 * @param {*} rawTravelTimes An array of the estimated travel time from each address
 */
function displayAsPieChart(rawTravelTimes) {
    console.log("display as pie chart", rawTravelTimes.length);

    dict = processRawTimes(rawTravelTimes);
    console.log(dict);

    timeRanges = $.map(dict, function (value, key) { return key + " minutes" });
    timeCounts = $.map(dict, function (value, key) { return value });


    var sum = 0;
    for (time of rawTravelTimes) {
        sum += time;
    }
    avg = sum / rawTravelTimes.length;
    console.log("Average Commute Time:", avg);
    $("#averageBlock").show();
    $("#avg").text(String(Math.round(avg)) + " Minutes");

    $("#chartContainer").show();

    var ctx = document.getElementById('chart-area').getContext('2d');
    var myPieChart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                data: timeCounts,
                backgroundColor: [
                    'rgb(153, 255, 51)',
                    'rgb(102, 255, 204)',
                    'rgb(255, 204, 0)',
                    'rgb(255, 102, 0)',
                    'rgb(255, 0, 0)',
                ],
                label: 'Commute Times'
            }],
            labels: timeRanges
        },
        options: Chart.defaults.pie,
    });
}

var marker;
var map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: { lat: 59.325, lng: 18.070 }
    });

    marker = new google.maps.Marker({
        map: map,
        draggable: true,
        animation: google.maps.Animation.DROP,
        position: { lat: 59.327, lng: 18.067 }
    });
}

function displayMap(place, outputJson) {
    //Create a geocoder
    geocoder = new google.maps.Geocoder();

    // set the center of the map to the office location
    map.setCenter(place.geometry.location);
    //put a unique marker there.
    var marker = new google.maps.Marker({
        position: place.geometry.location,
        map: map,
        title: 'Proposed Office Location',
        icon: {
            url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
          }
      });

      for (address of outputJson) {
          console.log("Addr:", address);
          geocoder.geocode(
            {
                address: address.addresses
            },
            (results, status) => {
                if (status === "OK") {
                    console.log("Success");
                    new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location
                    });
                } else { /*
                    alert(
                        "Geocode was not successful for the following reason: " + status
                    ); */
                }
            }
          );
      }
    
      setTimeout(() => {  $("#mapContainer").show();}, 1000);

}
