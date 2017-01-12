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


    $('#save-collection-form').submit(function(){
        var theForm = $(this);

             // send xhr request
             $.ajax({
                 type: theForm.attr('method'),
                 url: theForm.attr('action'),
                 data: theForm.serialize(),
                 success: function(data) {
                     if(data.status == "Success"){
                          $('#collection-save-modal').modal('hide');
                          $('#current-collection').text('Current Collection Name :'+data.collection_name);
                          $('#current-collection').show();
                     }else {
                        $('#collection-save-modal .alert').remove();
                        $('#collection-save-modal .form-group').append('<div class="alert alert-warning alert-dismissible" role="alert" id="save-collection-error" ><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Error!</strong> Collection name must be unique. Choose another one.</div>');

                     }
                 }
             });

             // prevent submitting again
             return false;
        });
});

