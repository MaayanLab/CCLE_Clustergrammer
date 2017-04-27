var tmp_num;
var cat_colors;

// cgm = {};

var hzome = ini_hzome();

default_args = {};
default_args.row_tip_callback = hzome.gene_info;
default_args.matrix_update_callback = matrix_update_callback;
default_args.dendro_callback = dendro_callback;
default_args.sidebar_width = 135;

d3.select('.blockMsg').select('h1').text('Please wait...');

var viz_size = {'width':1140, 'height':750};

$(document).ready(function(){
    $(this).scrollTop(0);
});

// make_heatmaps('haematopoietic_and_lymphoid_tissue');
// make_heatmaps('bone');


window.onscroll = function() {

  var show_col_sim = 200;
  var show_row_sim = 1200;
  var hide_clust = 900;
  var hide_col_sim = 1800;
  var inst_scroll = $(document).scrollTop();

}

function make_heatmaps(inst_type){

  d3.select('#tissue_title')
    .html(function(){
      return  'Tissue Expression: ' + inst_type.toUpperCase();
    })

  d3.selectAll('#container-id div').remove();

  // <div class='wait_message'>Please wait ...</div>

  d3.select('#container-id')
    .append('div')
    .classed('wait_message', true)
    .html('Please wait ...');

  clust_name = 'json/intra-norm_'+ inst_type + '.json';

  d3.json(clust_name, function(network_data){

    var args = $.extend(true, {}, default_args);
    args.cat_colors = {};

    args.root = '#container-id';

    args.network_data = network_data;
    cgm = Clustergrammer(args);
    d3.select(cgm[inst_type].params.root+' .wait_message').remove();
  });

}

function matrix_update_callback(){
  console.log('matrix_update_callback')
  if (genes_were_found){
    enr_obj.clear_enrichr_results();
  }
}

function dendro_callback(inst_selection){

  var clust_num = this.root.split('-')[2];

  var inst_data = inst_selection.__data__;

  // toggle enrichr export section
  if (inst_data.inst_rc === 'row'){

    if (clust_num !== '2'){
      d3.selectAll('.enrichr_export_section')
        .style('display', 'block');
    } else {

      d3.selectAll('.enrichr_export_section')
        .style('display', 'none');
    }

  } else {
    d3.selectAll('.enrichr_export_section')
      .style('display', 'none');
  }

}
