$(document).ready(function(){
    // Variables from context
    var url_location = '{{location}}'
    var image = '{{image.id}}'
    var trig = '{{trigger}}'
    
//*********************************************//
// TRIGGERS FOR MODAL
// If the trigger value in the url is 1 reset
// the fade on the modal otherwise remove it
//*********************************************//

    if ('{{trigger}}' == '1'){
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
    }

//*********************************************//
// BULLETIN PAGE
// Heart not nested in bulletin page so it takes
// different targeting to function
//*********************************************//

    if(url_location == 'bulletin'){
        
        $('body').on('click', '.fa-heart', function(){
            var img_id = $(this).attr('id');
            var title = $(this).attr('title');
            if(title != 'Pet Loves'){

                $.ajax({
                    cache: false,
                    type:"GET",
                    url: `/process_heart/${img_id}/{{location}}`,
                })
                .done(function(data){
                    $(`#replace${img_id}`).html(data);                    
                })
                .fail(function(data){
                    console.log("Error in fetching data");
                })
            }
            
        });


        $('body').on('click', 'p button', function(){
            console.log('click')
            var img_id = $(this).attr('id');
            var url_location = '{{location}}'
            var loadurl =`/${url_location}/{{session_user.id}}/${img_id}/0`
            window.history.pushState({}, '', loadurl)
            window.location.reload();
        })



        $('body').on('click', '.post .post_comment button', function(e){
            var img_id = $(this).attr('id');
            var token = '{{csrf_token}}';
            var url_location = '{{location}}'
            var form_id = `.form_img_id${img_id}`
            var form_text = `.form_text${img_id}`
            var form_compnt = `.form_compnt${img_id}`
    
            e.preventDefault()
            $.ajax({
                cache: false,
                headers: { "X-CSRFToken": token },  
                type:'POST',
                data : { image_id :$(`${form_id}`).val(), component: $(`${form_compnt}`).val(), text: $(`${form_text}`).val()},
                url: `/process_add_comment/{{location}}`,
            })
            .done(function(data){
                    $(`#post${img_id}`).html(data);  
                    console.log('success')                                    
            })
            .fail(function(data){
                console.log("Error in fetching data");
            })

        });

        $('#comment_modal button').click(function(){
            var img_id = $(this).attr('id');
            var url_location = '{{location}}'
            var loadurl =`/${url_location}/{{session_user.id}}/${img_id}/0`
            window.history.pushState({}, '', loadurl)
            window.location.reload();


        })
    
    }
            

//*********************************************//
//  WHEN HIDING MODAL
//  When clicking off of the modal and it hides
//  adds the fade class back to the modal for
//  next time it is called on a new image
//*********************************************//

    $("#comment_modal").on('hidden.bs.modal', function(e){
            loadurl = `/${url_location}/{{session_user.id}}/0/0`
            window.history.pushState({}, '', loadurl)
            $('#comment_modal').addClass('fade');
    });
            


//*********************************************//
// WHEN CLICKING THE IMAGE
// When image is clicked it checks of the user is
// over the heart button using the heart boolean. 
// If so it makes an AJAX request get data to
// update the stats elements to represent new status
//*********************************************//        

    $('.dimage').click(function(){

        var img_id = $(this).attr('id');
        var replace = `#replace${img_id}` 
        var title = $(this).attr('title');
        if(heart == true){
            $.ajax({
            cache: false,
            type:"GET",
            url: `/process_heart/${img_id}/{{location}}`,
            })
            .done(function(data){
                $(`#replace${img_id}`).html(data);                    
            })
            .fail(function(data){
                console.log("Error in fetching data");
            })
        }
        
    })
    

//*********************************************//
// ON MOUSEENTER
// When mouse enters the image it tracks if the mouse
// is over the heart button or not useing the heart
// bool and corresponding mouse enter mouse outs
//*********************************************//

    $( '.dimage' )
    .mouseenter(function() {
        // Declare Variables needed 
        var img_id = $(this).attr('id');
        var img = `.open_modal${img_id}`
        var stats = `#stat${img_id}`
        var replace = `#replace${img_id}`

        // Sets headers to an opacity of .99  so that they will mainain
        // their heirarchy
        $(".opacity").css('opacity', '.99');

        // Return URL with image ID to push for loading modal
        if ('{{clicked_user}}' != ''){
            loadurl = `/${url_location}/{{clicked_user.id}}/${img_id}`
        } else {
            loadurl = `/${url_location}/{{session_user.id}}/${img_id}`
        }

        // Decreases the opacity of the image.
        $( `${img}`)
        .css('opacity', '.6')
        // When image is clicked it pushes new URL and reloads page
        // to show modal. Work around to make modal appear as a chat
        .click(function(){
            window.history.pushState({}, '', loadurl+'/1')
            window.location.reload()          
        });

        // COMMENT ICON needs different opacity. Will DRY UP later
        $( `${img}x`).css('opacity', '1') 
        .click(function(){
            window.history.pushState({}, '', loadurl+'/1')
            window.location.reload()          
        });

        // Show the stats
        $(`${stats}`).show()

        // Toggle heart boolean
        $('.fa-heart')
        .mouseenter(function(){
            heart = true;            
        })
        .mouseleave(function(){
            heart = false;
        })

    });

//*********************************************//
// ON MOUSEOUT
// Return image to normal opacity and hide stats
//*********************************************//

    $( ".dimage" )
    .mouseleave(function() {
        var id = $(this).attr('id');
        var stats = `#stat${id}`
        var img = `.open_modal${id}`

        $( `${img}`).css('opacity', '1')
        $(`${stats}`).hide()
    });


});