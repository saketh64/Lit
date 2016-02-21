var socket = io.connect('http://' + document.domain + ':' + location.port);

function create_song(title, url) {
    var ret = $("<div></div>");
    var result = $("<div class='row'></div>");
    var container = $("<div class = 'col-xs-6 col-sm-6 col-md-5 col-md-offset-2'></div>")
    var title = $("<h5 class = 'song_title'>" + title + "</h5>");

    var votes_container = $("<div class = 'col-xs-1 col-xs-offset-3 col-sm-1 col-sm-offset-4 col-md-2 col-md-offset-2 votes-container'>");
    var upvote_button = $("<img id='" + url + "' src='static/img/up_arrow_black.png' class='vote_button' onclick='clickUpvote(this);' onmouseover='hoverUpvote(this);' onmouseout='unhoverUpvote(this);'></img>");
    var downvote_button = $("<img id='" + url + "' src='static/img/down_arrow_black.png' class='vote_button' onclick='clickDownvote(this);' onmouseover='hoverDownvote(this);' onmouseout='unhoverDownvote(this);'></img>");


    votes_container.append(upvote_button).append(downvote_button);

    container.append(title);

    result.append(container).append(votes_container);

    ret.append(result);
    ret.append("<hr id='song_divider'>");

    return ret;
}

function create_search_result(title, id) {
    var result = $("<div class='row'></div>");
    var container = $("<div class = 'col-xs-6 col-sm-6 col-md-5 col-md-offset-2'></div>")
    var title = $("<h5 class = 'search_title' id = " + id  + ">" + title + "</h5>");

    var plus_container = $("<div class = 'col-xs-1 col-xs-offset-3 col-sm-1 col-sm-offset-4 col-md-2 col-md-offset-2'>");
    var plus = $("<img src='static/img/plus.png' class='add_plus_pic' id =" + id + "></img>");

    plus_container.append(plus);

    container.append(title);

    result.append(container).append(plus_container);

    return result;
}

function add(_title, _url) {
    // this is what an 'add' event looks like
    socket.emit('add', {
        title: _title,
        url: _url,
    });
}

function search(_query) {
    // this is what a search event looks like
    socket.emit('search', {
        query: _query
    });
}

function upvote(_url) {
    // this is what an upvote event looks like
    socket.emit('upvote', {
        url: _url
    });
}

function downvote(_url) {
    // this is what a downvote event looks like
    socket.emit('downvote', {
        url: _url
    });
}
var urls = [];

socket.on('update_list', function (message) {
    $('.song_container').empty();

    for(var i = 0;i < message.length;i++)
    {
        // TODO: populate queue of songs
        var current_song = message[i];
        $('.song_container').append(create_song(current_song["title"], current_song["url"]));
    }
});

socket.on('search_results', function (message) {
    $('.search_results').empty();
    urls = [];
    for(var i = 0;i < message.length;i++)
    {
        // TODO: populate search results
        var song = message[i];
        urls[i] = song["url"];
        $('.search_results').append(create_search_result(song["title"], i));
    }
});



$('.search-icon').click(function(){
    search($('#search-input input').val());
});

$(document).on('click', '.add_plus_pic', function(){
    var id = $(this).attr("id");
    var title = $(document.getElementById(id)).text();

    add(title, urls[id]);
    $('#search-modal').fadeOut(200);



});

function clickUpvote(element) {
    upvote(element.getAttribute('id'));
}
function clickDownvote(element) {
    downvote(element.getAttribute('id'));
}
function hoverUpvote(element) {
    element.setAttribute('src', 'static/img/up_arrow_blue.png');
}
function unhoverUpvote(element) {
    element.setAttribute('src', 'static/img/up_arrow_black.png');
}
function hoverDownvote(element) {
    element.setAttribute('src', 'static/img/down_arrow_blue.png');
}
function unhoverDownvote(element) {
    element.setAttribute('src', 'static/img/down_arrow_black.png');
}
