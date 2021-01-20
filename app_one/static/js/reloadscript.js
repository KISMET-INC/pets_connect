$(document).ready(function(){


    //*********************************************//
    // Set starting variables
    //*********************************************//
    $(".opacity").css('opacity', '.99');
    var heart = false;
    var selfclick = false;  //may not need
    var session_user = '';
    var image_list = [];
    var heart_sum = 0;

    //*********************************************//
    // Get URL Route variables
    //*********************************************//
    map = window.location.pathname.toString()
    map = map.split('/')
    console.log(map)

    var url_location = map[1]
    var clicked_user_id = map[2]
    var image = parseInt(map[3])


     //*********************************************//
    // Alert on Logout
    //*********************************************//
    $('.logout').on('click',function(){
        alert('Thank you for visiting Pets-Connect! We hope you saw some pets as "PAW-SOME" as yours! Come back soon to collect your  \u2661 hearts \u2661, and see the new pets that have been added! See you and your fur-kids soon!')
     })

    //*********************************************//
    // scrollToBottom()
    // When called scrolls into view element with id 'bottom'
    //*********************************************//

    function scrollToBottom() {
        if(document.body.contains(document.getElementById('bottom'))){
            $(".comments").scrollTop($('.comments')[0].scrollHeight);
        }
    }

    //*********************************************//
    // Close guest Message
    //*********************************************//

    $('.close_guest_message').on('click', function(){

            $('.guest_message').remove()
    })

    //*********************************************//
    // Close Modal on 'x' click
    //*********************************************//
    $('body').on('click', '.close_modal', function(){
        $('#comment_modal').modal('hide');
    })


    //*********************************************//
    // Pull Session_user_id from database
    //*********************************************//
    function get_session_id(){
        $.ajax({
            cache: false,
            type:"GET",
            url: `/get_session_id`,
        })
        .done(function(data){
            session_user =  data           
        })
        .fail(function(data){
            console.log("Error in fetching data");
        });
    }


    //*********************************************//
    // Pull Image List from database
    //*********************************************//
    function get_image_list(user_id){
        $.ajax({
            cache: false,
            type:"GET",
            url: `/get_image_list/${user_id}`,
        })
        .done(function(data){
            image_list =  data           
        })
        .fail(function(data){
            console.log("Error in fetching data");
        });
    }

    //*********************************************//
    // Pull Heart Sum from DB
    //*********************************************//
    function get_heart_sum(img_id){
        $.ajax({
            cache: false,
            type:"GET",
            url: `/get_heart_sum/${img_id}`,
        })
        .done(function(data){
            heart_sum =  data 
            $('.heart_sum').html(data)
            console.log(heart_sum)
                
        })
        .fail(function(data){
            console.log("Error in fetching data");
        });
    }


    //*********************************************//
    // MOBILE DEVICE 
    // On click toggle opacity and stat behaviour
    //*********************************************//

    if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)){
        $('body').on('click', '.dimage', function(){

            var img_id = $(this).attr('id');
            var img = `.open_modal${img_id}`
            var stats = `#stat${img_id}`
            
            // if heart was not clicked toggle dimage opacity and stat show
            if(heart == false && selfclick == false){
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
                
        });
    
    //*********************************************//
    // FOR DESKTOP AND LAPTOP
    // Mousover / Mouseout Behavior
    //*********************************************//
    } else {
        $( '.dimage' )
            .mouseenter(function() {
                
               // Declare Variables needed 
                var img_id = $(this).attr('id');
                var img = `.open_modal${img_id}`
                var stats = `#stat${img_id}` 
                $( `${img}`).css('opacity', '.6')
                $(`${stats}`).show()
            })

            .mouseleave(function() {
                var id = $(this).attr('id');
                var stats = `#stat${id}`
                var img = `.open_modal${id}`

                $( `${img}`).css('opacity', '1')
                $(`${stats}`).hide()
            });
        }  
        
        // END DEVICE DEPENDENT INSTRUCTIONS


        //*********************************************//
        // Process Heart Clicks
        //*********************************************//
        $('body').on('click', '.fa-heart', function(){
            heart = true;
            var img_id = $(this).attr('id');
            var img = `.open_modal${img_id}`
            var title = $(this).attr('title');
            var stats = `#stat${img_id}`
            get_session_id()
            
            // Stops the ability to like your own pet
            if(title == 'Your Pet Loves' && session_user.session_user_name != 'guest'){
                heart = false;
                $(`${img}`).css('opacity', '.6')
                $(`${stats}`).show()
                
            } else {
                // Process adding heart to image
                $.ajax({
                    cache: false,
                    type:"GET",
                    url: `/process_heart/${img_id}/${url_location}`,
                })
                .done(function(data){
                    if(url_location == 'bulletin'){
                        $(`#post${img_id}`).html(data);  
                    } else {
                        $(`#replace${img_id}`).html(data); 
                        get_heart_sum(img_id)          
                    }
                    heart = false;   
                })
                .fail(function(data){
                    console.log("Error in fetching data");
                })
            }
            
        }); // END PROCESS HEART CLICKS

        //*********************************************//
        // Process Follow Clicks
        //*********************************************//
        $('body').on('click', '.fa-podcast', function(){
            heart = true;
            var user_id = $(this).attr('user_id');
            var img_id = $(this).attr('image_id');
            get_session_id()
            
            $.ajax({
                cache: false,
                type:"GET",
                url: `/process_follow/${user_id}/${img_id}`,
            })
            .done(function(data){
                if(url_location != 'bulletin'){
                    for(var i = 0; i <  image_list.images.length; i++){
                        
                        $(`#replace${image_list.images[i]}`).html(data)
                    }
                } else {
                    $(`#post${img_id}`).html(data);  
                }
                heart = false;   
            })
            .fail(function(data){
                console.log("Error in fetching data");
            })
            
            
        }); // END PROCESS FOLLOW CLICKS


        //*********************************************//
        // COMMENT ICON - ON CLICK
        //*********************************************//
        $('body').on('click', 'p button', function(){
            var img_id = $(this).attr('id');
            $.ajax({
                cache: false,
                type:"GET",
                url: `/replace_modal/${img_id}`,
            })
            .done(function(data){

                $(`#replaceModal`).html(data);
                $('#comment_modal').modal('show');
                $("#comment_modal").on('shown.bs.modal', function(){
                    scrollToBottom()
                })

                //*********************************************//
                // WHEN MODAL IS HIDDEN update background elements
                //*********************************************//
                $("#comment_modal").on('hide.bs.modal', function(){
                    var url;

                    if (url_location == 'bulletin'){
                        url = `/replace_post/${img_id}`
                    } else {
                        url =  `/replace_image/${img_id}`
                    }

                    $.ajax({
                        cache: false,
                        type:"GET",
                        url: url,
                    })
                    .done(function(data){

                        if (url_location == 'bulletin'){
                            $(`#post${img_id}`).html(data); 
                        } else {
                            $(`.dashboard #${img_id}`).html(data)
                        }
                        
                    })
                    .fail(function(data){
                        console.log("Error in fetching data");
                    })
                });
            })
            .fail(function(data){
                console.log("Error in fetching data");
            })
        }); // END ON CLICK COMMENT ICON 

        //*********************************************//
        // Process DELETE COMMENT on X click
        //*********************************************//
        $('body').on('click', '.delete_comment', function(){
            var comment_id = $(this).attr('id');
            var img_id = $(this).attr('img');
            var component = $(this).attr('comp')
            var url;
            if ( $(this).hasClass( "from_post" )){
                url = `/process_delete_comment/${comment_id}/from_post`
            } else {
                url = `/process_delete_comment/${comment_id}/from_modal`
            }
        
            $.ajax({
                cache: false,
                type:'GET',
                url: url,
            })
            .done(function(data){
                
                if (component == 'from_post'){
            
                    $(`#post${img_id}`).html(data); 

                } else {
                    
                    $('#replace_comments').html(data)                                  
                    scrollToBottom()
                }
            })
            .fail(function(data){
                console.log("Error in fetching data");
            })

        }); // END DELETE COMMENT


        //*********************************************//
        // Process ADD COMMENT on POST Click
        //*********************************************//
        $('body').on('click', '.comment_form button', function(e){
           e.preventDefault()
            var img_id = $(this).attr('id');
            var component = $(this).attr('comp')
            // get informatin from form classes
            var form_id = `.form_img_id${img_id}${component}`
            var form_text = `.form_text${img_id}${component}`
            var form_compnt = `.form_compnt${img_id}${component}`

            $.ajax({
                cache: false,
                headers: { "X-CSRFToken": csrftoken },  
                type:'POST',
                data : { image_id :$(`${form_id}`).val(), component: component, text: $(`${form_text}`).val()},
                url: `/process_add_comment`,
            })
            .done(function(data){
                if( $(`${form_compnt}`).val() == 'from_post'){
                    $(`#post${img_id}`).html(data);   
                } else {
                    $('#replace_comments').html(data)                                  
                    scrollToBottom()
                }
                $(`${form_text}`).val("")
            })
            .fail(function(data){
                console.log("Error in fetching data");
            })
        });

});