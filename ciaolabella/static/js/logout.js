var closing_window = false;

$(window).on('focus', function () {
    closing_window = false;
 });
$(window).on('blur', function () {
    closing_window = true;
	if (!document.hidden) { //when the window is being minimized
		closing_window = false;
	}
	$(window).on('resize', function (e) { //when the window is being maximized
		closing_window = false;
	});
	$(window).off('resize'); //avoid multiple listening
 });
$('html').on('mouseleave', function () {
	closing_window = true;
 });
$('html').on('mouseenter', function () {
    closing_window = false;
});
$(document).on("click", "a", function () {
	closing_window = false;
});
$(document).on("click", "button", function () {
    closing_window = false;
});
$(document).on("submit", "form", function () {
    closing_window = false;
});
$(document).on("click", "input[type=submit]", function () {
    closing_window = false;
});

function logOut2() {
    $.ajax({
        url: '/member/logout2/',
        method: 'post',
        async: false
    });
};

window.addEventListener('unload', function (e) {
    if (closing_window) {
            logOut2();
    }
});