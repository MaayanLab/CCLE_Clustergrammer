
console.log('making CCLE tree')

var tree = {
  "children": [
    {
      "name": "THYROID",
      "size": 12
    },
    {
      "name": "SALIVARY GLAND",
      "size": 2
    },
    {
      "name": "SOFT TISSUE",
      "size": 21
    },
    {
      "name": "HAEMATOPOIETIC AND LYMPHOID TISSUE",
      "size": 180
    },
    {
      "name": "BILIARY TRACT",
      "size": 8
    },
    {
      "name": "PANCREAS",
      "size": 44
    },
    {
      "name": "CENTRAL NERVOUS SYSTEM",
      "size": 69
    },
    {
      "name": "BONE",
      "size": 29
    },
    {
      "name": "LARGE INTESTINE",
      "size": 61
    },
    {
      "name": "AUTONOMIC GANGLIA",
      "size": 17
    },
    {
      "name": "PLEURA",
      "size": 11
    },
    {
      "name": "URINARY TRACT",
      "size": 27
    },
    {
      "name": "LUNG",
      "size": 187
    },
    {
      "name": "BREAST",
      "size": 59
    },
    {
      "name": "SKIN",
      "size": 62
    },
    {
      "name": "OVARY",
      "size": 52
    },
    {
      "name": "PROSTATE",
      "size": 8
    },
    {
      "name": "KIDNEY",
      "size": 36
    },
    {
      "name": "UPPER AERODIGESTIVE TRACT",
      "size": 32
    },
    {
      "name": "STOMACH",
      "size": 38
    },
    {
      "name": "ENDOMETRIUM",
      "size": 27
    },
    {
      "name": "OESOPHAGUS",
      "size": 26
    },
    {
      "name": "LIVER",
      "size": 28
    }
  ]
}

var scale_tree = 1.05;

var width = 910*scale_tree, // innerWidth-40
    height = 530*scale_tree, // innerHeight-40,
    color = d3.scale.category20c(),
    div = d3.select("#tree_container").append("div")
       .attr('id','new_div')
       .style("position", "relative");

var treemap = d3.layout.treemap()
    .size([width, height])
    .sticky(true)
    .value(function(d) { return d.size; });


var node = div.datum(tree).selectAll(".node")
      .data(treemap.nodes)
      .enter().append("div")
      .attr("class", "node")
      .on('click',function(d){

        var clean_name = d.name.replace(/ /g, '_').toLowerCase();

        console.log(clean_name);


      })
      .attr('title', function(d) { return d.children ? null : d.name; })
      .call(position)
      .style("background-color", function(d) {
          return d.name == 'tree' ? '#fff' : color(d.name); })
      .append('div')
      .style("font-size", function(d) {
          // compute font size based on sqrt(area)
          return Math.max(12, 0.15*Math.sqrt(d.area))+'px'; })
      .text(function(d) { return d.children ? null : d.name; })

function position() {
  this.style("left", function(d) { return d.x + "px"; })
      .style("top", function(d) { return d.y + "px"; })
      .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
      .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; });
}


// make visualization now so that tooltips are positioned correctly
make_heatmaps('bone');
