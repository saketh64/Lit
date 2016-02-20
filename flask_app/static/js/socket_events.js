var socket = io.connect('http://' + document.domain + ':' + location.port);

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

socket.on('search_results', function (message) {
    for(var i = 0;i < message.length;i++)
    {
        
    }
});