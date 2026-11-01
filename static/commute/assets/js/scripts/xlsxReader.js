/*
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.7.7/xlsx.core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xls/0.7.4-a/xls.core.min.js"></script>
*/

var outputJson = null;
var titleName = null;
var rawTravelTimes = [];
var map;

function upload(place) {
    var filename = $('#excelfile').val().toLowerCase();
    //Check for html5 by checking if FileReader exists
    if (typeof (FileReader) != "undefined") {
        var reader = new FileReader();

        reader.onload = function(data) {
            //define what happens when the file is loaded
            data = data.target.result;
            if (filename.endsWith(".xlsx")) {
                var workbook = XLSX.read(data, { type: 'binary' });
                var sheetName = workbook.SheetNames[0];
                titleName = workbook.Sheets[sheetName]['A1'].v;
                outputJson = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
            }
            else if (filename.endsWith(".xls")) {
                var workbook = XLS.read(data, { type: 'binary' });
                var sheetName = workbook.SheetNames[0];
                titleName = workbook.Sheets[sheetName]['A1'];
                outputJson = XLS.utils.sheet_to_json(workbook.Sheets[sheetName]);
            } else {
                alert("This is not an excel file.");
            }
            console.log("On Load called");
            console.log(outputJson);
        }

        reader.onloadend = function(data) {
            checkResults(data, place);
        }

        reader.readAsArrayBuffer($("#excelfile")[0].files[0]);
        var output = $("#exceldiv").text();
        //console.log(output);
        return output;
    } else {
        alert("Your browser does not support html5.");
    }
}



function checkResults(results, place) {
    if (outputJson != null && titleName != null) {
        for (address of outputJson) {
            console.log(address);
            console.log(place);
            processStuff(address.addresses, place.formatted_address);
        }
        console.log(outputJson.length);

        //rawTravelTimes.push(21);
        //rawTravelTimes.push(35);
        setTimeout(() => {  displayMap(place, outputJson); }, 1000);
        setTimeout(() => {  displayAsPieChart(rawTravelTimes); }, 1000);
        
    } else {
        alert("Javascript Error: Please alert the website designers.")
    }
}

function processStuff(address, hq) {
    console.log("test");
    var service = new google.maps.DistanceMatrixService;

    service.getDistanceMatrix({
        origins: [address],
        destinations: [hq],
        travelMode: 'DRIVING',
        unitSystem: google.maps.UnitSystem.METRIC,
        avoidHighways: false,
        avoidTolls: false
      }, distanceMatrixCallback);
}

function distanceMatrixCallback(response, status) {
    if (status !== 'OK') {
      alert('Error was: ' + status);
    } else {
      var originList = response.originAddresses;
      var destinationList = response.destinationAddresses;
      rawTravelTimes.push(response.rows[0].elements[0].duration.value/60);
      console.log(rawTravelTimes);
    }
  }