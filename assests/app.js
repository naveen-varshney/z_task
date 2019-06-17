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
  $("#sumbit-date").attr("disabled", true);
  $.ajax({
                url: '/refresh',
                type: 'get',
                data:{'for_date': x},
                success: function(data){
                    var data = JSON.parse(data);
                    var for_date = data.for_date;
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
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    var errorMsg = 'Ajax request failed: ' + xhr.responseText;
                    $('#t-body').html(errorMsg);
                  }
  });
  $("#sumbit-date").attr("disabled", false);
}

function LoadEquity(search='') {
  $.ajax({
                url: '/get_top_equity',
                type: 'get',
                data:{'search': search},
                success: function(data){
                    var data = JSON.parse(data);
                    var for_date = data.for_date;
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
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    var errorMsg = 'Ajax request failed: ' + xhr.responseText;
                    $('#t-body').html(errorMsg);
                  }
            });
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
