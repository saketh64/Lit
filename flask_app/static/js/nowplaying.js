var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.emit('on_connect', {
    party_url: window.location.href
});
socket.emit('nowplaying_connect', {
    party_url: window.location.href
});

socket.on('heartbeat_to_client', function (message) {
    socket.emit('heartbeat_to_server', {});
});

$(".button-row").css("margin-top", new_height());

function new_height() {
    return $(window).height() / 4;
}

// This will be an HTML5 Audio object (will NOT be in the DOM)
var audio;
var is_playing = false;

var progress_bar;

$(document).ready(function () {
    // bind events for play/pause click
    var playButton = document.getElementById("play-button");
    playButton.addEventListener("click", playpause_click);

    progress_bar = $("#progressBar");
});

function playpause_click() {
    if (is_playing == true) {
        $("#play-button").css("background-image", "url(static/img/pause.png)");
        audio.play();
    } else {
        $("#play-button").css("background-image", "url(static/img/play.png)");
        audio.pause();
    }

    is_playing = !is_playing;
}

function progress(percent) {
    var progressBarWidth = percent * progress_bar.width() / 100;

    progress_bar.find('div').animate({
        width: progressBarWidth
    });
}

socket.on('new_song', function (message) {
    if (message) {
        console.log(message["id"]);
        var id = message["id"];

        var audio_file_path = "/static/music/" + message["id"] + ".mp3";

        audio = new Audio(audio_file_path);
        audio.ontimeupdate = progress_update;
        audio.onended = song_ended;
        audio.play();
        $('#progressBar').show();

        $('.current_song_title').text(message["title"]);
    } else {
        $('.current_song_title').text("No song is playing");
    }

});

var progress_update = function () {
    var current_time = audio.currentTime;
    var total_time = audio.duration;
    var progress_pct = 100 * (current_time / total_time);
    console.log(current_time + "/" + total_time + " = " + progress_pct);
    progress(progress_pct);
}

var song_ended = function () {
    // probably just needed when debugging, but might as well always call this
    audio.src = ""
    audio.ontimeupdate = null;
    audio.onended = null;
    audio = null;

    $('#progressBar').hide();


    console.log("Emitting 'song_end' event.");
    socket.emit('song_end', {
        party_url: window.location.href
    });
}

$('body').keydown(function (e) {
    if (e.keyCode == 32) { // play/pause
        playpause_click();
    }
})