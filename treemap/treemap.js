var filePath = "../data/genius_hip_hop_lyrics.csv"
var defaults = {
    margin: {top: 24, right: 0, bottom: 0, left: 0},
    rootname: "TOP",
    format: ",d",
    title: "",
    width: 960,
    height: 500
};


d3.select("#chart").append("svg")
.attr("height", defaults.height)
.attr("width", defaults.width)

d3.csv(filePath, function(error, data) {
  console.log(data);
  var nested_data = d3.nest()
       				.key(function(d)  { return d.candidate; })
       				.key(function(d)  { return d.sentiment; })
              .key(function(d)  { return d.artist; })
				      .entries(data);

			// Creat the root node for the treemap
			var root = {};

			// Add the data to the tree
			root.key = "Data";
			root.values = nested_data;

			console.log(nested_data);

			loadData(root);

});
