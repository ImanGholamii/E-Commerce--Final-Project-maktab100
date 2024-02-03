$(document).ready(function () {

    $(".edit-profile-button a").on("click", function (event) {
        event.preventDefault();
        var target = $("#edit-profile-section");
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top
            }, 1000);
        }
    });
});
