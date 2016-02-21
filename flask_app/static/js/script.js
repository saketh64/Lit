
$(document).ready(function() {

	$('#add_song').click(function() {
		$('#search-modal').fadeIn(200);
		$('#search-input-field').focus();
	});

	$('.close-icon').click(function(){
		$('#search-modal').fadeOut(200)
	});




});
