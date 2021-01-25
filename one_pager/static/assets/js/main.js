$(document).ready(function() {
	//Preloader
	preloaderFadeOutTime = 500;
	function hidePreloader() {
		var preloader = $('.spinner-wrapper');
		preloader.fadeOut(preloaderFadeOutTime);
	}
	hidePreloader();
});

$(document).ready(function() {
	$("#top").click(function(){
		$('html, body').animate({scrollTop:0}, 'slow');
		return false;
	});
});

function hide(elementId) { 
	document.getElementById(elementId).style.display="none";
}

// ===== Scroll to Top ==== 
$(window).scroll(function() {
	if ($(this).scrollTop() >= 50) {    // If page is scrolled more than 50px
		$('#top').fadeIn("fast");       // Fade in the arrow
	} else {
		$('#top').fadeOut("fast");      // Else fade out the arrow
	}
});	

let outer = document.querySelector("#outer");
let content = outer.querySelector('#content');

repeatContent(content, outer.offsetWidth);

let el = outer.querySelector('#loop');
el.innerHTML = el.innerHTML + el.innerHTML;

function repeatContent(el, till) {
	let html = el.innerHTML;
	let counter = 0; // prevents infinite loop

	while (el.offsetWidth < till && counter < 100) {
		el.innerHTML += html;
		counter += 1;
	}
}
 
function refreshPage () {
	var page_y = document.getElementsByTagName("body")[0].scrollTop;
	window.location.href = window.location.href.split('?')[0] + '?page=' + page_y;
}
window.onload = function () {
	setTimeout(refreshPage, 35000);
	if ( window.location.href.indexOf('page') != -1 ) {
		var match = window.location.href.split('?')[1].split("&")[0].split("=");
		document.getElementsByTagName("body")[0].scrollTop = match[1];
	}
}
