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
    // Split URL string to extract useful variables into
    // an array 
    //*********************************************//
    map = window.location.pathname.toString()
    map = map.split('/')

    var url_location = map[1]
    var clicked_user_id = map[2]

    $(window).scroll(function() {
        if($(window).scrollTop() >= $(document).height() - $(window).height()-1) {
            get_more_images()
        }
    });

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
        $('body').on('mouseover', '.dimage', function(){
                
               // Declare Variables needed 
                var img_id = $(this).attr('id');
                var img = `.open_modal${img_id}`
                var stats = `#stat${img_id}` 
                $( `${img}`).css('opacity', '.6')
                $(`${stats}`).show()
            })

            .on('mouseleave', '.dimage', function(){
                var id = $(this).attr('id');
                var stats = `#stat${id}`
                var img = `.open_modal${id}`

                $( `${img}`).css('opacity', '1')
                $(`${stats}`).hide()
            });
        }  
        
        // END DEVICE DEPENDENT INSTRUCTIONS


    //*********************************************//
    // Search
    //*********************************************//
    $('.search').on('click', function(e){

        e.preventDefault()
        var user_email = $('.search_email').val()
        var list = $('#search_modal .users_modal').attr('list')
        var user_id = $('#search_modal .users_modal').attr('user_id')
        

        $.ajax({
            cache: false,
            headers: { "X-CSRFToken": csrftoken },  
            type:'POST',
            data : { user_email : user_email, list: list, user_id: user_id},
            url: `/search`,
        })
        .done(function(data){
            console.log(data)
            if(data == 'None'){
                $('.error').html("Email Not Found")
            } else {
                window.location.href = data  
            }
        })
        .fail(function(data){
            console.log("Error in fetching data");
        });

    })

    //*********************************************//
    // WHEN Search Modal is shown insert correct querylist
    //*********************************************//

        $('.search_btn').on('click', function(){
            url='';
            if($(this).html() == 'All Pet Owners'){
                $('.modal-title').html("Search All Pet Owners")
                url = "/get_all_users_list"
            } else {
                $('.modal-title').html("Search Your Followers")
                url = "/get_followers_list"
            }

            $("#search_modal").on('show.bs.modal', function(){
                $.ajax({
                    cache: false,
                    type:"GET",
                    url: url,
                })
                .done(function(data){
                        $(`#search_modal .modal-body`).html(data);     
                })
                .fail(function(data){
                    console.log("Error in fetching data");
                });
            })

        })
    
    

    //*********************************************//
    // On EDIT ICON CLICK
    // Show Edit Input - Hide comment elements behind
    //*********************************************//
    $('body').on('click', '.fa-pen', function(e){
        var comment_id = $(this).attr('id')
        var new_comment = $(`.edit_comment_text_${comment_id}`).val()
        //Reset and show all comments and hide all inputs when
        //user clicks another comment
        $(`.comm_text`).show()
        $(`.comm_edit`).hide()
        
        $(`.eform${comment_id}`).css('display','flex').show()
        $(`.single_comment #comment${comment_id}`).hide()

        // On CANCEL CLICK - re-show text / hide edit input
        $('body').on('click', '.edit_comment_cancel', function(e){
            e.preventDefault()
            var comment_id = $(this).attr('comm_id')
            $(`.comm_text`).show()
            
            $(`.edit_comment_text_${comment_id}`).val(new_comment)
            $(`.eform${comment_id}`).hide()
    
            $(`.single_comment #comment${comment_id}`).show()
        })
        
    })

    //*********************************************//
    // On EDIT COMMENT SUBMIT BUTTON CLICK
    //*********************************************//
    $('body').on('click', '.edit_comment_btn', function(e){
        e.preventDefault()
        var comment_id = $(this).attr('comm_id')
        var image_id = $(this).attr('img_id')
        var new_comment = $(`.edit_comment_text_${comment_id}`).val()
        var component = $(this).attr('comp')
        $.ajax({
            cache: false,
            headers: { "X-CSRFToken": csrftoken },  
            type:'POST',
            data : { text : new_comment, component : component, image_id : image_id},
            url: `/process_edit_comment/${comment_id}`,
        })
        .done(function(data){
            if( component == 'from_post'){
                $(`#post${image_id}`).html(data);   
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

    //*********************************************//
    // Hide COMMENT EDIT INPUTS on load
    //*********************************************//
    $('.comm_edit').hide()

    //*********************************************//
    // WHEN SEARCH MODAL IS HIDDEN clear previous errors
    //*********************************************//
    $("#search_modal").on('hide.bs.modal', function(){
        $('.error').html("")
    })

    
    //*********************************************//
    // get more images
    //*********************************************//
    function get_more_images() {

        $.ajax({
            cache: false,
            type:"GET",
            url: `/get_more_images`,
        })
        .done(function(data){
            if (data != 'none'){

                $(`#get_more`).append(data);
                        
            }
                
        })
        .fail(function(data){
            console.log("Error in fetching data");
        });

    }
    //*********************************************//
    // OPEN LOADER ON AJAX START
    //*********************************************//
    // $(document).ajaxStart(function(){
    //     $('.loader').show();
    // });
    // $(document).ajaxStop(function(){
    // $('.loader').hide();
    // });

    //*********************************************//
    // Alert on Logout
    //*********************************************//
    // $('.logout').on('click',function(){
    //     alert('Thank you for visiting Pets-Connect! We hope you saw some pets as "PAW-SOME" as yours! Come back soon to collect your  \u2661 HEARTS \u2661, and see the new pets that have been added! See you and your fur-kids soon!')
    //  })

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
    });

    //*********************************************//
    // Close Modal on 'x' click
    //*********************************************//
    $('body').on('click', '.close_modal', function(){
        $('#comment_modal').modal('hide');
    });

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
            get_image_list(user_id)
            
            $.ajax({
                cache: false,
                type:"GET",
                url: `/process_follow/${user_id}/${img_id}`,
            })
            .done(function(data){
                if(url_location != 'bulletin'){
                    for(var i = 0; i <  image_list.images.length; i++){
                        $(`.hide_icon${image_list.images[i]}`).hide()
                    }
                    $(`#replace${img_id}`).html(data)
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
