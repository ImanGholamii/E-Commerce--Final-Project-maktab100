$(document).ready(function () {

  $(".nav-link").on("click", function () {

    $('html, body').animate({
      scrollTop: $("#filters_menu").offset().top
    }, 1000);
  });
});
