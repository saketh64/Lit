var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('new_song', function (message){
	if (message)
	{
		$('.current_song_title').text(message["title"]);
	}
	else
	{
			$('.current_song_title').text("No song is playing");
	}
});

// only called on initial guest.html page load
socket.on('now_playing_song_title', function (message){
		if (message)
		{
			$('.current_song_title').text(message["title"]);
		}
		else
		{
				$('.current_song_title').text("No song is playing");
		}
});

$(document).ready(function() {
    $('#add_song').click(function() {
        $('#search-modal').fadeIn(200);
        $('#search-input-field').focus();
		$('#blur_wrapper').addClass('blur');
    });

    $('.close-icon').click(function(){
		$('#blur_wrapper').removeClass('blur');
        $('#search-modal').fadeOut(200)
    });

    $('#search-input-field').keydown(function(e) {
        if (e.keyCode == 13) {
            $('.search-icon').click();
        }
    });

    $('.search-icon').click(function(){
        search($('#search-input input').val());
    });
});
