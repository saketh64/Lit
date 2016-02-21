var socket = io.connect('http://' + document.domain + ':' + location.port);

$(document).ready(function() {

	$('#add_song').click(function() {
		$('.search_modal').fadeIn(200);
	});

	$('.close').click(function(){
		$('.search_modal').fadeOut(200)
	});




});

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
