$(document).ready(function() {
      $("body").prepend('<div id="cover" style="z-index: 1001; display: none;"></div>');

    $('#search-form').submit(function() {
        var pass = true;
        //some validations

        if(pass == false){
            return false;
        }
        $("#cover").show();

        return true;
    });
    $('.add-to-collection-btn').click(function(){
        var current_collection = $('#current-collection').val();
        if(current_collection == undefined | current_collection.length == 0){
                $('#error-message-dlg').modal('show');
        }
    });

    $('.view-btn').click(function(){
        var current_collection = $('#current-collection').val();
        if(current_collection == undefined | current_collection.length == 0){
                $('#error-message-dlg').modal('show');
        }
    });

});

