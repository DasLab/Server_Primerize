$(document).ready(function () {
	$("#footer").load("/res/html/footer.html");
	$("[data-toggle='popover']").popover({trigger:"hover"}); 
	$("[data-toggle='tooltip']").tooltip(); 
});