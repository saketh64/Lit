var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('heartbeat_to_client', function (message) {
  socket.emit('heartbeat_to_server', {});
});

// Inject YouTube API script
var tag = document.createElement('script');
tag.src = "//www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

$(".button-row").css("margin-top", new_height());

function new_height () {
	return $(window).height()/4;
}

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

var play = false;
function onPlayerReady(event) {
  
  // bind events
  var playButton = document.getElementById("play-button");
  playButton.addEventListener("click", function() {

  	if(play == true)
  	{
  		$("#play-button").css("background-image", "url(static/img/pause.png)");
  		player.playVideo();
  	}
  	else
  	{
  		$("#play-button").css("background-image", "url(static/img/play.png)");
  		player.pauseVideo();
  	}

  	play = !play;    
  });
}

function progress(percent, $element) {
  var progressBarWidth = percent * $element.width() / 100;

// $element.find('div').animate({ width: progressBarWidth }, 500).html(percent + "%&nbsp;");

  $element.find('div').animate({ width: progressBarWidth });
}

function onPlayerStateChange(event) {
	if (event.data == 0) {
		socket.emit('song_end', {});
	}

  if (event.data == YT.PlayerState.PLAYING) {

      $('#progressBar').show();
      var playerTotalTime = player.getDuration();

      mytimer = setInterval(function() {
        var playerCurrentTime = player.getCurrentTime();

        var playerTimeDifference = (playerCurrentTime / playerTotalTime) * 100;


        progress(playerTimeDifference, $('#progressBar'));
      }, 1000);        
    } else {
      
      clearTimeout(mytimer);
    }
}


 socket.on('new_song', function (message){
    console.log(message["url"]);
    var contents = message["url"].split('/watch?v=');
    var newsrc = contents[0] + "/embed/" + contents[1] + "?autoplay=1";
    player.loadVideoByUrl(newsrc);
    $('.current_song_title').text(message["title"]);
  });


