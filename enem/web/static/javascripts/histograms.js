jQuery(function($) {
  var histogramArea = $("#histogram");
  var histogram = new Histogram();

  function fetchGrade(url) {
    $.ajax({
      dataType: "json",
      url: url
    }).done(function(data) {
      histogram.addItem(data.name, data);
      histogram.draw(histogramArea);
    }).error(function() {
      alert("Erro ao carregar dados.");
    });
  }

  $("[name='city_code']").on("change", function() {
    var cityCode = $(this).val();
    fetchGrade("/cities/" + cityCode);
  }).trigger("change");

  $("[name='school_code']").on("change", function() {
    var schoolCode = $(this).val();
    fetchGrade("/schools/" + schoolCode);
  });
});
