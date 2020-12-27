$( ".dimage" )
.mouseover(function() {
    var id = $(this).attr('id');
    var img = `.open_modal${id}`
    var stats = `#stat${id}`
    $("#TOP_long").css('opacity', '.99');
    $(".heading").css('opacity', '.99');
    $( `${img}`).css('opacity', '.6').click(function(){
        window.location = `/explore/${id}`
    });
    $(`${stats}`).show()
});

$( ".dimage" )
.mouseleave(function() {
    var id = $(this).attr('id');
    var stats = `#stat${id}`
    var img = `.open_modal${id}`
    $( `${img}`).css('opacity', '1')
    $(`${stats}`).hide()
});