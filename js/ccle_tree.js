
console.log('making CCLE tree')

var tree = {
  "children": [
    {
      "mongo_id": "57db082c0329ef78ffc9b490",
      "name": "THYROID",
      "size": 12
    },
    {
      "mongo_id": "57db082e0329ef78ffc9b491",
      "name": "SALIVARY GLAND",
      "size": 2
    },
    {
      "mongo_id": "57db08330329ef78ffc9b492",
      "name": "SOFT TISSUE",
      "size": 21
    },
    {
      "mongo_id": "57db08400329ef78ffc9b493",
      "name": "HAEMATOPOIETIC AND LYMPHOID TISSUE",
      "size": 180
    },
    {
      "mongo_id": "57db08570329ef78ffc9b498",
      "name": "BILIARY TRACT",
      "size": 8
    },
    {
      "mongo_id": "57db08490329ef78ffc9b495",
      "name": "PANCREAS",
      "size": 44
    },
    {
      "mongo_id": "57db08500329ef78ffc9b496",
      "name": "CENTRAL NERVOUS SYSTEM",
      "size": 69
    },
    {
      "mongo_id": "57db08550329ef78ffc9b497",
      "name": "BONE",
      "size": 29
    },
    {
      "mongo_id": "57db08450329ef78ffc9b494",
      "name": "LARGE INTESTINE",
      "size": 61
    },
    {
      "mongo_id": "57db085a0329ef78ffc9b499",
      "name": "AUTONOMIC GANGLIA",
      "size": 17
    },
    {
      "mongo_id": "57db085c0329ef78ffc9b49a",
      "name": "PLEURA",
      "size": 11
    },
    {
      "mongo_id": "57db08600329ef78ffc9b49b",
      "name": "URINARY TRACT",
      "size": 27
    },
    {
      "mongo_id": "57db086b0329ef78ffc9b49c",
      "name": "LUNG",
      "size": 187
    },
    {
      "mongo_id": "57db086f0329ef78ffc9b49d",
      "name": "BREAST",
      "size": 59
    },
    {
      "mongo_id": "57db08730329ef78ffc9b49e",
      "name": "SKIN",
      "size": 62
    },
    {
      "mongo_id": "57db08790329ef78ffc9b49f",
      "name": "OVARY",
      "size": 52
    },
    {
      "mongo_id": "57db087c0329ef78ffc9b4a0",
      "name": "PROSTATE",
      "size": 8
    },
    {
      "mongo_id": "57db08810329ef78ffc9b4a1",
      "name": "KIDNEY",
      "size": 36
    },
    {
      "mongo_id": "57db08850329ef78ffc9b4a2",
      "name": "UPPER AERODIGESTIVE TRACT",
      "size": 32
    },
    {
      "mongo_id": "57db088b0329ef78ffc9b4a3",
      "name": "STOMACH",
      "size": 38
    },
    {
      "mongo_id": "57db088f0329ef78ffc9b4a4",
      "name": "ENDOMETRIUM",
      "size": 27
    },
    {
      "mongo_id": "57db08920329ef78ffc9b4a5",
      "name": "OESOPHAGUS",
      "size": 26
    },
    {
      "mongo_id": "57db08970329ef78ffc9b4a6",
      "name": "LIVER",
      "size": 28
    }
  ]
}

var scale_tree = 1.05;

var width = 955*scale_tree, // innerWidth-40
    height = 650*scale_tree, // innerHeight-40,
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

        // console.log(d.name);
        // console.log(d.size);
        // console.log(d.mongo_id)
        // console.log('\n')
        // // location.href='/clustergrammer/viz/'+d.mongodb
        // qs = '?col_label= CCLE '+  d.name + ' Cell Lines&row_label=Genes'
        // redirect_url = '/clustergrammer/viz/'+d.mongo_id+'/'+'CCLE: '+d.name+qs;
        // window.open(redirect_url, '_blank');

        // console.log(redirect_url)

        console.log('clicking');

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

