var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('heartbeat_to_client', function (message) {
	socket.emit('heartbeat_to_server', {});
	console.log("emitted");
});
console.log("hi");
