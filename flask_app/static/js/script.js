
$(document).ready(function() {
	function create_song(title) {
	    var result = $("<div class='row'></div>");
	    var container = $("<div class = 'col-xs-6 col-sm-6 col-md-5 col-md-offset-2'></div>")
	    var title = $("<h5 class = 'song_title'>" + title + "</h5>");

	    var votes_container = $("<div class = 'col-xs-1 col-xs-offset-3 col-sm-1 col-sm-offset-4 col-md-2 col-md-offset-2'>");
	    var upvote_button = $("<img src='static/img/up_arrow_black.png' class='vote_button'></img>");
	    var downvote_button = $("<img src='static/img/down_arrow_black.png' class='vote_button'></img>");


	    votes_container.append(upvote_button).append(downvote_button);

	    container.append(title);

	    result.append(container).append(votes_container);

	    return result;
	}

	function create_search_result(title) {
	    var result = $("<div class='search_result'></div>");
	    var title = $("<h5>" + title + "</h5>");
	    var add_button = $("<img src='static/img/plus.png' class='add_button'></img>");

	    result.append(title).append(add_button);

	    return result;
	}

	$('.add_song_button').click(function() {
		$('.search_modal').fadeIn(200);
	});

	$('.close').click(function(){
		$('.search_modal').fadeOut(200)
	});

	var song = create_song("Testing this");
	$('.container.song_container').append(song);


});

