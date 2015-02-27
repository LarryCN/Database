$(document).ready(function() {
	$("#about-btn").click( function(event) {
		msgstr = $("#msg").html()
        msgstr = msgstr + "o"
        $("#msg").html(msgstr)
 	});
	$(".ouch").click( function(event) {
    	alert("You clicked me! ouch!");
	});
	$("p").hover( function() {
        $(this).css('color', 'red');
    },
    function() {
        $(this).css('color', 'blue');
    });
});
