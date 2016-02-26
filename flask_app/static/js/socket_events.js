var socket = io.connect('http://' + document.domain + ':' + location.port);

var urls = [];

/* EVENTS TO BACKEND */
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
    console.log("upvoting "+_url);
    socket.emit('upvote', {
        url: String(_url)
    });
}

function downvote(_url) {
    // this is what a downvote event looks like
    console.log("downvoting "+_url);
    socket.emit('downvote', {
        url: String(_url)
    });
}
/* ~~~~~~~~~~~~~~~~~~~~ */

/* EVENTS FROM BACKEND */
socket.on('update_list', function (message) {
    $('.song_container').empty();
    var my_user_id;
    if (!(my_user_id = Cookies.get('user_id'))) {
        console.log("User doesn't have an ID cookie.");
    }
    if (message["queue"].length > 0) {
        $(".next_song_title").empty();
        $(".next_song_title").append(message["queue"][0]["title"]);
    } else {
        $(".next_song_title").empty();
        $(".next_song_title").append("No songs are queued.");
    }
    for(var i = 0;i < message["queue"].length;i++)
    {
        var current_song = message["queue"][i];
        var upvoted = false;
        var downvoted = false;
        for (var j = 0;j < current_song.upvote.length;j++)
        {
          if (current_song.upvote[j] == my_user_id)
          {
            console.log("Detected a user vote on "+current_song["url"])
            upvoted = true
            break;
          }
        }
        
        for (var j = 0;j < current_song.downvote.length;j++)
        {
          if (current_song.downvote[j] == my_user_id)
          {
            console.log("Detected a user vote on "+current_song["url"])
            downvoted = true
            break;
          }
        }
        $('.song_container').append(create_song(current_song["title"], current_song["url"],upvoted,downvoted));
    }
});

socket.on('connect', function() {
    socket.emit('connected');
});

socket.on('search_results', function (message) {
    console.log("Search returned to user: "+message["user_id"]);
    if(message["user_id"] != Cookies.get('user_id'))
      return;


    $('.search_results').empty();
    urls = [];
    for(var i = 0;i < message["search_results"].length;i++)
    {
        // TODO: populate search results
        var song = message["search_results"][i];
        urls[i] = song["url"];
        $('.search_results').append(create_search_result(song["title"], i));
    }
});
/* ~~~~~~~~~~~~~~~~~~~~~~~ */

/* GENERATE HTML */
function create_song(title, url, upvoted, downvoted) {
    var row_container = $("<div class='row_container'></div>");
    var song_title_container = $("<div class = 'song_title_container'></div>")
    var title = $("<h5 class = 'song_title'>" + title + "</h5>");

    var upvote_button = $("<img id='" + url + "' src='static/img/up_arrow_black.png' class='vote_button_up' onclick=\"upvote(this.getAttribute('id'));\"></img>");
    if (upvoted)
    {
      upvote_button.attr('src', 'static/img/up_arrow_blue.png');
    }
    var downvote_button = $("<img id='" + url + "' src='static/img/down_arrow_black.png' class='vote_button_down' onclick=\"downvote(this.getAttribute('id'));\"></img>");
    if (downvoted)
    {
      downvote_button.attr('src', 'static/img/down_arrow_blue.png');
    }

    song_title_container.append(title);
    row_container.append(song_title_container);
    row_container.append(upvote_button);
    row_container.append(downvote_button);
    row_container.append("<hr id='song_divider'>");

    return row_container;
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
/* ~~~~~~~~~~~~~~~~~~~~ */

/* LISTENERS */
$(document).on('click', '.add_plus_pic', function(){
    var id = $(this).attr("id");
    var title = $(document.getElementById(id)).text();
    add(title, urls[id]);
    $('#blur_wrapper').removeClass('blur');
    $('#search-modal').fadeOut(200);
});
/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
