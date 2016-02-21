var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('heartbeat_to_client', function (message) {
	socket.emit('heartbeat_to_server', {});
});


// Inject YouTube API script
var tag = document.createElement('script');
tag.src = "//www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;

function onYouTubePlayerAPIReady() {
  // create the global player from the specific iframe (#video)
  player = new YT.Player('video', {
    events: {
      // call this function when player is ready to use
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

function onPlayerReady(event) {
  
  // bind events
  var playButton = document.getElementById("play-button");
  playButton.addEventListener("click", function() {
    player.playVideo();
  });
  
  var pauseButton = document.getElementById("pause-button");
  pauseButton.addEventListener("click", function() {
    player.pauseVideo();
  });
  
}

function onPlayerStateChange(event) {
	if (event.data == 0) {
		socket.emit('song_end', {});
		console.log("reached");
	}
}

socket.on('new_song', function (message){
	var contents = message["url"].split('/watch?v=');
	var newsrc = contents[0] + "/embed/" + contents[1] + "?autoplay=1";
	$('#video').attr('src', newsrc);
});

