var base_url = "http://127.0.0.1:8000/";

function refreshItems() {
  $.ajax({
           url : base_url+'api/entries/0/',
           datatype : 'json',
           success : function(data, textStatus, XMLHttpRequest){
             console.log(data);
             console.log(textStatus);
           },
           error : function(XMLHttpRequest, textStatus, errorThrown) {
             console.log(XMLHttpRequest);
             console.log(textStatus);
             console.log(errorThrown);
           }
         });
}

$(document).ready(function(){
                    $('#nojs').remove();
                    setInterval ( "refreshItems()", 5000 );
                  });