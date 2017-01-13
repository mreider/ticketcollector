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
        var current_collection = $('#current-collection').text();
        console.log(current_collection);
        if(current_collection == undefined | current_collection.trim().length == 0){
                $('#error-message-dlg').modal('show');
        }else {
            var modal = $('#ticket-details-modal');
            var url = $(this).data('url');
            $.ajax({
                url:url,
                context: document.body
            }).done(function(response) {
//                console.log(response);
                modal.html(response);
                $(modal).modal('show');
            });
        }
    });


    $('#save-collection-form').submit(function(){
        var theForm = $(this);
        var search_string = $('#search').val();
        $('#save-collection-form #search_criteria').remove();
        $('<input>').attr({
                        type: 'hidden',
                         id: 'search_criteria',
                         name: 'search_criteria',
                         value: search_string
                    }).appendTo(theForm);
             // send xhr request
             $.ajax({
                 type: theForm.attr('method'),
                 url: theForm.attr('action'),
                 data: theForm.serialize(),
                 success: function(data) {
                     console.log(data);
                     if(data.status == "Success"){
                          $('#collection-save-modal').modal('hide');
                          $('#current-collection').text('Current Collection Name :'+data.collection_name);
                          $('#current-collection-id').val(data.collection_id);
                          $('#current-collection').show();
                          $('#search').attr('disabled','disabled');
                          $('#search-btn').attr('disabled','disabled');
                          $('#save-btn').attr('disabled','disabled');
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

$(document).ajaxStart(function () {
    $("#cover").show();
  })
  .ajaxStop(function () {
    $("#cover").hide();
  });