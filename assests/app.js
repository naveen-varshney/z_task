$(document).ready(function(){
    setTimeout(function(){
      // fetch top 10 stock
      LoadEquity();
    },100); // milliseconds

    $("#search").on("keyup", function() {
      var value = $(this).val().toUpperCase();
      console.log(value);
      // get all matched strock for search
      LoadEquity(search=value);
  });
});

$(document).ready(function(){
    setMaxDate();
});

function setMaxDate() {

  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth()+1; //January is 0!
  var yyyy = today.getFullYear();

  if(dd<10){
          dd='0'+dd
      }

      if(mm<10){
          mm='0'+mm
      }
  today = yyyy+'-'+mm+'-'+dd;
  document.getElementById("get-date").setAttribute("max", today);
}

function GetDate() {
  // get date field from input date field

  var x = document.getElementById("get-date").value;
  console.log(x);
  if (x == '') {
    return false;
  }
  $("#submit-date").attr("disabled", true);
  $.ajax({
                url: '/refresh',
                type: 'get',
                data:{'for_date': x},
                success: function(data){
                    var data = JSON.parse(data);
                    var for_date = data.for_date;
                    var top_10 = data.top_10
                    if (!data.success) {
                      $('#t-body').html("<h4>some error occured while fetching data!!</h4>");
                      return;
                    }

                    $('#t-body').empty();
                    if (search != '') {
                      $('#main-heading').html("Equity search results for <strong id='for-date'></strong>");
                    }
                    else{
                      $('#main-heading').html("Top 10 Equity Stock for <strong id='for-date'></strong>");
                    }
                    $('#for-date').html(for_date);
                    top_10.forEach(AddRowInTable);
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    var errorMsg = 'Ajax request failed: ' + xhr.responseText;
                    $('#t-body').html(errorMsg);
                  }
  });
  $("#submit-date").attr("disabled", false);
}

function LoadEquity(search='') {
  $.ajax({
                url: '/get_top_equity',
                type: 'get',
                data:{'search': search},
                success: function(data){
                    var data = JSON.parse(data);
                    var for_date = data.for_date;
                    if (!data.success) {
                      $('#t-body').html("some error occured while fetching data!!");
                      return;
                    }
                    var top_10 = data.top_10
                    $('#t-body').empty();
                    if (search != '') {
                      $('#main-heading').html("Equity search results for <strong id='for-date'></strong>");
                    }
                    else{
                      $('#main-heading').html("Top 10 Equity Stock for <strong id='for-date'></strong>");
                    }
                    $('#for-date').html(for_date);
                    top_10.forEach(AddRowInTable);
                    PreapreChart(data);
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    var errorMsg = 'Ajax request failed: ' + xhr.responseText;
                    $('#t-body').html(errorMsg);
                  }
            });
}

function PreapreChart(data) {
  var myConfig = {
  "type":"scatter",
  "title":{
    "text":"Top Stocks for " + data.for_date
  },
  "plot": {
    "tooltip": {
      "text": "Name %kt and Code %vt."
    }
  },
  "scale-y":{
    "offset-start":"35%",
    "values":"0:10:2",
    "format":"%v",
    "label":{
      "text":"Highs"
    }
  },
  // "scale-y-2":{
  //   "blended":true,
  //   "offset-end":"75%",
  //   "placement":"default",
  //   "values":"0:3:3",
  //   "format":"%vM",
  //   "label":{
  //     "text":"Volume"
  //   }
  // },
  "series":[
    {
      "type":"stock",
      "scales":"scale-x,scale-y",
      "values":GetChartValues(data.top_10)
    }
  ]
  };

  zingchart.render({
  id : 'myChart',
  data : myConfig,
  height: 400,
  width: "100%"
  });
}

function GetChartValues(top_10) {
  var arr = []
  $.each(top_10, function( index, item ) {
    arr.push([item.Name,item.Code,item.Open,item.High,item.Low,item.Close,item.PreClose])
  });
  return arr
}

// create table cell for each item
function AddRowInTable(item) {
  document.getElementById("t-body").innerHTML += "<tr>"
    +"<td>"+item.Name  +"</td>"
    +"<td>"+ item.Code +"</td>"
    +"<td>"+ item.Open +"</td>"
    +"<td>"+ item.High +"</td>"
    +"<td>"+ item.Low +"</td>"
    +"<td>"+ item.Close +"</td>"
    +"<td>"+ item.PreClose +"</td>"
  +"</tr>";
}
