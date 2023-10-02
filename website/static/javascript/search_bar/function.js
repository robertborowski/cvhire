// -------------------------- start --------------------------
$("#ui_search_bar").keyup(function(){
  var currently_typed = $(this).val().toLowerCase();
  currently_typed = $.trim(currently_typed)

  var testList = $('.uiSearchItem');
  testList.each(function() {
    var i_category = $(this).text().toLowerCase();
    i_category = $.trim(i_category)
    // if (i_category == "aws")
    if (i_category.indexOf(currently_typed) >= 0) {
      //  block of code to be executed if the condition is true
      $( this ).removeClass("uiSearchItemInvisible");
      $( this ).addClass("uiSearchItemVisible2");
    } else {
      //  block of code to be executed if the condition is false
      $( this ).removeClass("uiSearchItemVisible2");
      $( this ).addClass("uiSearchItemInvisible");
    }
  });
});
// -------------------------- end --------------------------

// -------------------------- start --------------------------
$("#ui_search_bar_v2").keyup(function(){
  var currently_typed = $(this).val().toLowerCase();
  currently_typed = $.trim(currently_typed)

  var testList = $('.uiSearchItem_v2');
  testList.each(function() {
    var i_category = $(this).text().toLowerCase();
    i_category = $.trim(i_category)
    // if (i_category == "aws")
    if (i_category.indexOf(currently_typed) >= 0) {
      //  block of code to be executed if the condition is true
      $( this ).removeClass("uiSearchItemInvisible");
      $( this ).addClass("uiSearchItemVisible2");
    } else {
      //  block of code to be executed if the condition is false
      $( this ).removeClass("uiSearchItemVisible2");
      $( this ).addClass("uiSearchItemInvisible");
    }
  });
});
// -------------------------- end --------------------------