(function() {
  $(window).scroll(function() {
    var oVal;
    oVal = $(window).scrollTop() / 150;
    return $(".blurred-img").css("opacity", oVal);
  });

}).call(this);
