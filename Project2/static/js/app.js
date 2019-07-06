function buildCharts(sample) {
  d3.json(`/samples/${sample}`).then((data) => {

    const RegionName = data.RegionName;
    const May2019 = data.May2019;

    // Build a Bubble Chart
    var bubbleLayout = {
      margin: { t: 0 },
      hovermode: "closest",
      xaxis: { title: "City" }
    };
    var bubbleData = [
      {
        x: RegionName,
        y: May2019,
        text: RegionName,
        mode: "markers",
        marker: {
          size: May2019,
          color: May2019,
          // colorscale: "Earth"
        }
      }
    ];

    Plotly.newPlot("bubble", bubbleData, bubbleLayout);

    // Build a Pie Chart

    var pieData = [
      {
        values: May2019.slice(0, 10),
        labels: RegionName.slice(0, 10),
        hovertext: RegionName.slice(0, 10),
        hoverinfo: "hovertext",
        type: "pie"
      }
    ];

    var pieLayout = {
      // margin: { t: 0, l: 0 },
      title: "Top 10 Monthly Listing May 2019",
     };

    Plotly.newPlot("pie", pieData, pieLayout);
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/usstates").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    // buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  // buildMetadata(newSample);
}

// Initialize the dashboard
init();
