!function (a) {
    "use strict";
    a(function () {
        var b = a(window), c = a(document.body);
        c.scrollspy({target: ".plask-sidebar"}),
            b.on("load", function () {
                c.scrollspy("refresh")
            }), setTimeout(function () {}, 100);
    })
}(jQuery);

$(function() {
  $('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 300);
        return false;
      }
    }
  });
});