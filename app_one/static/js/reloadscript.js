$(document).ready(function(){
    
    $('body').on('click', '.close_modal', function(){
        $('#comment_modal').modal('hide');
    })

    function scrollToBottom() {
        if(document.body.contains(document.getElementById('bottom'))){
            var elmnt = document.getElementById("bottom");
            elmnt.scrollIntoView(false); // Bottom
        }
    }

    map = window.location.pathname.toString()
    map = map.split('/')
    console.log(map)

    var url_location = map[1]
    
    var clicked_user_id = map[2]
    var image = parseInt(map[3])
    var trig = map[4]
    var component = map[5]
    var session_user_id = ''
    var heart = false;
    var selfclick = false;

    $.ajax({
        cache: false,
        type:"GET",
        url: `/get_session_id`,
    })
    .done(function(data){
        session_user_id = data                 
    })
    .fail(function(data){
        console.log("Error in fetching data");
    });



    window.onpopstate = function(event) {
        $('#comment_modal').modal('hide');
   };



   


    // Check for mobile device
   if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)){
    // true for mobile device
        $('body').on('click', '.dimage', function(){
          
            $(".opacity").css('opacity', '.99');
            
            var img_id = $(this).attr('id');
            var img = `.open_modal${img_id}`
            var stats = `#stat${img_id}`
            
            if(heart == false && selfclick == false){
                console.log($(`${img}`).css('opacity'))
                if( $(`${img}`).css('opacity') != '1') {
                    $(`${img}`).css('opacity', '1')
                    $(`${stats}`).hide()
                } else {
                    $('img').css('opacity', '1');
                    $('.stats').hide()
                    $(`${img}`).css('opacity', '.6')
                    $(`${stats}`).show()
                }
            }
                    
            // Return URL with image ID to push for loading modal
            if (clicked_user_id != ''){
                loadurl = `/${url_location}/${clicked_user_id}/${img_id}`
            } else {
                loadurl = `/${url_location}/${session_user_id}/${img_id}`
            }

            // COMMENT ICON needs different opacity. Will DRY UP later
            $( `${img}x`).css('opacity', '1') 
            .click(function(){
                window.history.pushState({}, '', loadurl+'/1')
                window.location.reload()          
            });
                
        });

   }else{
    //false for not mobile device
        $( '.dimage' )
            .mouseenter(function() {
               // Declare Variables needed 
                var img_id = $(this).attr('id');
                var img = `.open_modal${img_id}`
                var stats = `#stat${img_id}`
                var replace = `#replace${img_id}`


                //Sets headers to an opacity of .99  so that they will mainain
               // their heirarchy
                $(".opacity").css('opacity', '.99');

                //Return URL with image ID to push for loading modal
                if (  clicked_user_id = ''){
                    loadurl = `/${url_location}/${clicked_user_id}/${img_id}`
                } else {
                    loadurl = `/${url_location}/${session_user_id}/${img_id}`
                }

                //Decreases the opacity of the image.
                $( `${img}`).css('opacity', '.6')
               // COMMENT ICON needs different opacity. Will DRY UP later
                $( `${img}x`).click(function(){
                    // window.history.pushState({}, '', loadurl+'/1')
                    // window.location.reload()          
                });

               // Show the stats
                $(`${stats}`).show()

            })
    //*********************************************//
    // ON MOUSEOUT
    // Return image to normal opacity and hide stats
    // //*********************************************//
        $( ".dimage" )
        .mouseleave(function() {
            var id = $(this).attr('id');
            var stats = `#stat${id}`
            var img = `.open_modal${id}`

            $( `${img}`).css('opacity', '1')
            $(`${stats}`).hide()
        });
    } // END DEVICE DEPENDENT INSTRUCTIONS

        // HEART //
        $('body').on('click', '.fa-heart', function(){
            // var url_location = '{{location}}'
            var img_id = $(this).attr('id');
            var img = `.open_modal${img_id}`
            var title = $(this).attr('title');
            var stats = `#stat${img_id}`
            heart = true;
        
            if(title == 'Your Pet Loves'){
                heart = false;
                $(`${img}`).css('opacity', '.6')
                $(`${stats}`).show()
                
            } else {

                $.ajax({
                    cache: false,
                    type:"GET",
                    url: `/process_heart/${img_id}/${url_location}`,
                })
                .done(function(data){
                    if(url_location != 'bulletin'){
                        $(`#replace${img_id}`).html(data);             
                    } else {
                        $(`#post${img_id}`).html(data);  
                    }
                    heart = false;   
                })
                .fail(function(data){
                    console.log("Error in fetching data");
                })
            }
            
        });

        //*********************************************//
        // COMMENT ICON - ON CLICK
        //*********************************************//
        $('body').on('click', 'p button', function(){
            var img_id = $(this).attr('id');
            // var url_location = '{{location}}'
            if(session_user_id == 1){
                var loadurl =`/${url_location}/${clicked_user_id}/${img_id}/1`
            } else {
                var loadurl =`/${url_location}/${session_user_id}/${img_id}/1`
            }
            var selfclick = true;
            // window.history.pushState({}, '', loadurl)
            // window.location.reload();
            $.ajax({
                cache: false,
                type:"GET",
                url: `/replace_modal/${img_id}`,
            })
            .done(function(data){

                $(`#replaceModal`).html(data);
                $('#comment_modal').modal('show');
                $("#comment_modal").on('shown.bs.modal', function(e){
                    scrollToBottom()
                 })
                
            })
            .fail(function(data){
                console.log("Error in fetching data");
            })
        });

        

        $('body').on('click', '.delete_comment', function(e){
            var img_id = $(this).attr('id');
            e.preventDefault()
            $.ajax({
                cache: false,
                type:'GET',
                url: `/process_delete_comment/${img_id}`,
            })
            .done(function(data){
                    $(`#post${img_id}`).html(data);  
                    console.log('success') 
                    $('#replace_comments').html(data)                                  
                    scrollToBottom()
            })
            .fail(function(data){
                console.log("Error in fetching data");
            })

        });

        $('body').on('click', '.post_comment button', function(e){
            var img_id = $(this).attr('id');
            
            var form_id = `.form_img_id${img_id}`
            var form_text = `.form_text${img_id}`
            var form_compnt = `.form_compnt${img_id}`

            e.preventDefault()
            $.ajax({
                cache: false,
                headers: { "X-CSRFToken": csrftoken },  
                type:'POST',
                data : { image_id :$(`${form_id}`).val(), component: $(`${form_compnt}`).val(), text: $(`${form_text}`).val()},
                url: `/process_add_comment`,
            })
            .done(function(data){
                    $(`#post${img_id}`).html(data);  
                    console.log('success') 
                    $('#replace_comments').html(data)                                  
                    scrollToBottom()
            })
            .fail(function(data){
                console.log("Error in fetching data");
            })

        });

        $('#comment_modal button').click(function(){
            var img_id = $(this).attr('id');
            // var url_location = '{{location}}'
            var loadurl =`/${url_location}/${session_user_id}/${img_id}/0`
            window.history.pushState({}, '', loadurl)
            window.location.reload();
        })

    //*********************************************//
    // TRIGGERS FOR MODAL
    // If the trigger value in the url is 1 reset
    // the fade on the modal otherwise remove it
    //*********************************************//

    if (trig == '1'){
        $('#comment_modal').addClass('fade'); 
    } else {
        $('#comment_modal').removeClass('fade');
    }

    //******************************************************//
    // IF CURRENT IMAGE
    // If there is a current image id in url when loading
    // show the modal containing the information on the image
    //******************************************************//

    if (image != 0 ){      
        $('#comment_modal').modal('show');
        var d = $('.comments');
        d.scrollTop(d.prop("scrollHeight"));
    }
            

    //*********************************************//
    //  WHEN HIDING MODAL
    //  When clicking off of the modal and it hides
    //  adds the fade class back to the modal for
    //  next time it is called on a new image
    //*********************************************//

    $("#comment_modal").on('hidden.bs.modal', function(e){
        alert('click')
        if(session_user_id == 1){
            loadurl = `/${url_location}/${session_user_id}/0/0`
        } else {
            loadurl = `/${url_location}/${clicked_user_id}/0/0`
        }
            window.history.pushState({}, '', loadurl)
            $('#comment_modal').addClass('fade');
    });
        
});