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
  }).trigger("change").attr("disabled", true);

  $("[name='school_code']").typeahead({
    remote: {
      url: "/schools/search?term=%QUERY",
      filter: function(response) {
        return response.schools.map(function(school) {
          return { value: school[1], code: school[0] }
        });
      }
    }
  }).on("typeahead:selected", function(event, school) {
    fetchGrade("/schools/" + school.code, function(data) {
      histogram.addItem("right", data);
      histogram.draw(histogramArea);
    });
  });
});
