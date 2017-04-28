console.log('loading heatmap');
var hzome = ini_hzome();

default_args = {};
default_args.row_tip_callback = hzome.gene_info;
default_args.matrix_update_callback = matrix_update_callback;
default_args.dendro_callback = dendro_callback;
default_args.sidebar_width = 140;

function make_clust(tissue_name){

  d3.selectAll('#clustergram_container div')
    .remove();

  d3.select('#clustergram_container')
    .append('div')
    .classed('wait_message', true)
    .style('font-size', '20px')
    .html('please wait ...');

  var clean_name = tissue_name.replace(/ /g, '_').toLowerCase();

  console.log(clean_name);

  d3.select('#tissue_title')
    .html(function(){
      return 'Tissue Expression: ' + tissue_name.toUpperCase();
    })

  // var clust_name = 'mult_view.json'
  var clust_name = 'json/intra-norm_' + clean_name + '.json'

  d3.json(clust_name, function(network_data){

    var args = $.extend(true, {}, default_args);

    args.root = '#clustergram_container';
    args.network_data = network_data;

    cgm = Clustergrammer(args);
    d3.select(cgm.params.root+' .wait_message').remove();

    check_setup_enrichr(cgm);

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
