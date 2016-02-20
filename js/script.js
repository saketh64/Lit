$(document).ready(function() {

	$('.add_song_button').click(function() {
		$('.search_modal').fadeIn(200);
	});

	$('.close').click(function(){
		$('.search_modal').fadeOut(200)
	});


});

function create_song(title) {
    var result = $("<div class='song'></div>");
    var title = $("<h5>" + title + "</h5>");
    var votes_container = $("<div class='votes_container'></div>");
    var upvote_button = $("<img src='TODO' class='vote_button'></img>");
    var downvote_button = $("<img src='TODO' class='vote_button'></img>");

    votes_container.append(upvote_button).append(downvote_button);

    result.append(title).append(votes_container);

    return result;
}

function create_search_result(title) {
    var result = $("<div class='search_result'></div>");
    var title = $("<h5>" + title + "</h5>");
    var add_button = $("<img src='img/plus.png' class='add_button'></img>");

    result.append(title).append(add_button);

    return result;
}
