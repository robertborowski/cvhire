$(document).ready(function() {
  // ----------------------------- general poll submission start -----------------------------
  $('input[name="ui_selection_radio"]').click(function() {
    if ($('input[name="ui_selection_radio"]:checked').length > 0) {
      $('#id-submit_enable_general_1').removeAttr('disabled');
      $('#id-submit_enable_general_1').attr('enabled', true);
      $('#id-submit_enable_general_2').removeAttr('disabled');
      $('#id-submit_enable_general_2').attr('enabled', true);
    } else {
      $('#id-submit_enable_general_1').removeAttr('enabled');
      $('#id-submit_enable_general_1').attr('disabled', true);
      $('#id-submit_enable_general_2').removeAttr('enabled');
      $('#id-submit_enable_general_2').attr('disabled', true);
    }
  });
  // ----------------------------- general poll submission end -----------------------------
  // ----------------------------- continue form start -----------------------------
  $("#id-flow_continue_1").click(function() {
    // part 1
    $("#id-form_part_1").removeClass("uiSearchItemVisible2");
    $("#id-form_part_1").addClass("uiSearchItemInvisible");
    // part 2
    $("#id-form_part_2").removeClass("uiSearchItemInvisible");
    $("#id-form_part_2").addClass("uiSearchItemVisible2");
    // flow div
    $(this).removeClass("uiSearchItemVisible2");
    $(this).addClass("uiSearchItemInvisible");
    // submit div
    $("#id-flow_submit_1").removeClass("uiSearchItemInvisible");
    $("#id-flow_submit_1").addClass("uiSearchItemVisible2");
  });
  // ----------------------------- continue form end -----------------------------
  // ----------------------------- activity details start -----------------------------
  // show info
  $("#id-flow_show_details_1").click(function() {
    $("#id-activity_details_1").removeClass("uiSelectAllBlockInvisible");
    $("#id-activity_details_1").addClass("uiSelectAllBlockVisible");
    $("#id-flow_hide_details_1").removeClass("uiSelectAllBlockInvisible");
    $("#id-flow_hide_details_1").addClass("uiSelectAllBlockVisible");
    $("#id-flow_show_details_1").removeClass("uiSelectAllBlockVisible");
    $("#id-flow_show_details_1").addClass("uiSelectAllBlockInvisible");
  });
  // hide info
  $("#id-flow_hide_details_1").click(function() {
    $("#id-activity_details_1").removeClass("uiSelectAllBlockVisible");
    $("#id-activity_details_1").addClass("uiSelectAllBlockInvisible");
    $("#id-flow_hide_details_1").removeClass("uiSelectAllBlockVisible");
    $("#id-flow_hide_details_1").addClass("uiSelectAllBlockInvisible");
    $("#id-flow_show_details_1").removeClass("uiSelectAllBlockInvisible");
    $("#id-flow_show_details_1").addClass("uiSelectAllBlockVisible");
  });
  // ----------------------------- activity details end -----------------------------
});