jQuery(function($) {
  var histogramArea = $("#histogram");
  var histogram = new Histogram();

  function fetchGrade(url, callback) {
    $.ajax({
      dataType: "json",
      url: url
    }).done(function(data) {
      callback(data);
    }).error(function() {
      alert("Erro ao carregar dados.");
    });
  }

  $("[name='city_code']").on("change", function() {
    var cityCode = $(this).val();
    fetchGrade("/cities/" + cityCode, function(data) {
      histogram.addItem("left", data);
      histogram.draw(histogramArea);
    });
  }).trigger("change");

  $("[name='school_code']").on("change", function() {
    var schoolCode = $(this).val();
    fetchGrade("/schools/" + schoolCode, function(data) {
      histogram.addItem("right", data);
      histogram.draw(histogramArea);
    });
  });
});
