(function() {
  var Histogram = function() {
    this.items = {};
  }

  /**
   * Adds an item to this histogram. If the item already exists, its
   * data will be replaced.
   * @param {String} id the item id
   * @param {Array} frequency the grades frequency
   */
  Histogram.prototype.addItem = function(id, frequency) {
    this.items[id] = frequency;
  }

  /**
   * Get the series data in a Highcharts compatible format.
   * @private
   * @return {Array} the series data
   */
  Histogram.prototype.getSeries = function() {
    var series = []

    for (var i in this.items) {
      var item = this.items[i];

      series.push({
        name: item.name,
        data: item.relativeGrades
      })
    }

    return series;
  }

  /**
   * Draws the histogram on the informed area.
   * @param {jQueryObject} container
   */
  Histogram.prototype.draw = function(container) {
    container.highcharts({
      chart: {
        type: "column"
      },
      title: {
        text: null
      },
      xAxis: {
        title: {
          text: "Frequência de notas"
        },
        labels: {
          formatter: function() {
            return this.value * 100;
          }
        }
      },
      yAxis: {
        min: 0,
        max: 100,
        title: {
          text: "Alunos (%)"
        },
        labels: {
          formatter: function() {
            return this.value + "%";
          }
        }
      },
      tooltip: {
        formatter: function() {
          return "<b>"+ this.series.name +"</b>: "+ this.y +"%";
        }
      },
      plotOptions: {
        column: {
          pointPadding: 0,
          groupPadding: 0,
          borderWidth: 0
        }
      },
      series: this.getSeries()
    });
  }

  window.Histogram = Histogram;
})();
