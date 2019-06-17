$(document).ready(function(){
    setTimeout(function(){
       LoadEquity();
     },1000); // milliseconds
});

function LoadEquity() {
  $.ajax({
                url: '/get_top_equity',
                type: 'get',
                success: function(data){
                    //If the success function is execute,
                    //then the Ajax request was successful.
                    //Add the data we received in our Ajax
                    //request to the "content" div.
                    debugger      
                    $('#content').html(data);
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    var errorMsg = 'Ajax request failed: ' + xhr.responseText;
                    $('#content').html(errorMsg);
                  }
            });
}
