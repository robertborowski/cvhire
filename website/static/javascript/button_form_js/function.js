// ------------------------------------- individual function start -------------------------------------
$(document).ready(function() {
  let radioSelected = false;
  let checkboxSelected = false;

  // one-role-many-cvs
  $('input[type="radio"][name="radio-one-role"]').on('change', function() {
    radioSelected = !!$('input[type="radio"][name="radio-one-role"]:checked').length;
    checkValidity();
  });
  $('input[type="checkbox"][name="checkbox-many-cvs"]').on('change', function() {
    checkboxSelected = !!$('input[type="checkbox"][name="checkbox-many-cvs"]:checked').length;
    checkValidity();
  });

  // one-cv-many-roles
  $('input[type="checkbox"][name="checkbox-many-roles"]').on('change', function() {
    checkboxSelected = !!$('input[type="checkbox"][name="checkbox-many-roles"]:checked').length;
    checkValidity();
  });
  $('input[type="radio"][name="radio-one-cv"]').on('change', function() {
    radioSelected = !!$('input[type="radio"][name="radio-one-cv"]:checked').length;
    checkValidity();
  });

  function checkValidity() {
    if (radioSelected && checkboxSelected) {
      $('#id_submit_button').prop('disabled', false);
    } else {
      $('#id_submit_button').prop('disabled', true);
    }
  }
});
// ------------------------------------- individual function end -------------------------------------

// ------------------------------------- individual function start -------------------------------------
$(document).ready(function() {
  // ------------------------------------- cv start -------------------------------------
  $('#id_cv_select_all').on('change', function() {
    if ($(this).is(':checked')) {
      // If "select all" checkbox is checked, uncheck all other checkboxes
      $('input[type="checkbox"]').not('#id_cv_select_all').prop('checked', false);
    }
  });
  // Optional: If any other checkbox is selected, you can auto-deselect the "select all" checkbox
  $('input[type="checkbox"]').not('#id_cv_select_all').on('change', function() {
    if ($(this).is(':checked')) {
      $('#id_cv_select_all').prop('checked', false);
    }
  });
  // ------------------------------------- cv end -------------------------------------
  // ------------------------------------- role start -------------------------------------
  $('#id_role_select_all').on('change', function() {
    if ($(this).is(':checked')) {
      // If "select all" checkbox is checked, uncheck all other checkboxes
      $('input[type="checkbox"]').not('#id_role_select_all').prop('checked', false);
    }
  });
  // Optional: If any other checkbox is selected, you can auto-deselect the "select all" checkbox
  $('input[type="checkbox"]').not('#id_role_select_all').on('change', function() {
    if ($(this).is(':checked')) {
      $('#id_role_select_all').prop('checked', false);
    }
  });
  // ------------------------------------- role end -------------------------------------
});
// ------------------------------------- individual function end -------------------------------------

// ------------------------------------- individual function start -------------------------------------
$(document).ready(function() {

  // Wrap the logic inside a function for reusability
  function handleRadioChange() {
    var selectedValue = $('input[name="radioSubscriptionOption"]:checked').val();

    if (selectedValue === "monthly") {
      $("#id-monthly_price").addClass("uiSearchItemVisible");
      $("#id-monthly_price").removeClass("uiSearchItemInvisible");
      $("#id-yearly_price").addClass("uiSearchItemInvisible");
      $("#id-yearly_price").removeClass("uiSearchItemVisible");
    } else if (selectedValue === "yearly") {
      $("#id-monthly_price").addClass("uiSearchItemInvisible");
      $("#id-monthly_price").removeClass("uiSearchItemVisible");
      $("#id-yearly_price").addClass("uiSearchItemVisible");
      $("#id-yearly_price").removeClass("uiSearchItemInvisible");
    }
  }

  // Call the function initially to set things up
  handleRadioChange();

  // Bind the change event to the radio buttons
  $('input[name="radioSubscriptionOption"]').change(handleRadioChange);
});
// ------------------------------------- individual function end -------------------------------------

// ------------------------------------- individual function start -------------------------------------
$(document).ready(function() {
  // ------------------------------------- edit button start -------------------------------------
  // Attach a click event handler to the div with id="id-edit_grade_btn"
  $('#id-edit_grade_btn').on('click', function() {
      // Add class 'class_a' to the div with id="id-edit_grade_section"
      $('#id-edit_grade_section').addClass('uiSearchItemVisible');
      $('#id-edit_grade_section').removeClass('uiSearchItemInvisible');
      $('#id-hide_grade_btn').addClass('uiSearchItemVisible');
      $('#id-hide_grade_btn').removeClass('uiSearchItemInvisible');

      // Remove class 'class_b' from the div with id="id-edit_grade_btn"
      $(this).addClass('uiSearchItemInvisible');
      $(this).removeClass('uiSearchItemVisible');
  });
  // ------------------------------------- edit button end -------------------------------------
  // ------------------------------------- hide button start -------------------------------------
  // Attach a click event handler to the div with id="id-edit_grade_btn"
  $('#id-hide_grade_btn').on('click', function() {
    // Add class 'class_a' to the div with id="id-edit_grade_section"
    $('#id-edit_grade_section').addClass('uiSearchItemInvisible');
    $('#id-edit_grade_section').removeClass('uiSearchItemVisible');
    $('#id-edit_grade_btn').addClass('uiSearchItemVisible');
    $('#id-edit_grade_btn').removeClass('uiSearchItemInvisible');

    // Remove class 'class_b' from the div with id="id-edit_grade_btn"
    $(this).addClass('uiSearchItemInvisible');
    $(this).removeClass('uiSearchItemVisible');
});
// ------------------------------------- hide button end -------------------------------------
});
// ------------------------------------- individual function end -------------------------------------

// ------------------------------------- individual function start -------------------------------------
$(document).ready(function() {
  // ------------------------------------- edit button start -------------------------------------
  // Attach a click event handler to the div with id="id-edit_grade_btn"
  $('#id-edit_followups_btn').on('click', function() {
      // Add class 'class_a' to the div with id="id-edit_grade_section"
      $('#id-followups_str_section').addClass('uiSearchItemInvisible');
      $('#id-followups_str_section').removeClass('uiSearchItemVisible');
      $('#id-followups_input_section').addClass('uiSearchItemVisible');
      $('#id-followups_input_section').removeClass('uiSearchItemInvisible');
      $('#id-hide_followups_btn').addClass('uiSearchItemVisible');
      $('#id-hide_followups_btn').removeClass('uiSearchItemInvisible');

      // Remove class 'class_b' from the div with id="id-edit_grade_btn"
      $(this).addClass('uiSearchItemInvisible');
      $(this).removeClass('uiSearchItemVisible');
  });
  // ------------------------------------- edit button end -------------------------------------
  // ------------------------------------- hide button start -------------------------------------
  // Attach a click event handler to the div with id="id-edit_grade_btn"
  $('#id-hide_followups_btn').on('click', function() {
    // Add class 'class_a' to the div with id="id-edit_grade_section"
    $('#id-followups_str_section').addClass('uiSearchItemVisible');
    $('#id-followups_str_section').removeClass('uiSearchItemInvisible');
    $('#id-followups_input_section').addClass('uiSearchItemInvisible');
    $('#id-followups_input_section').removeClass('uiSearchItemVisible');
    $('#id-edit_followups_btn').addClass('uiSearchItemVisible');
    $('#id-edit_followups_btn').removeClass('uiSearchItemInvisible');

    // Remove class 'class_b' from the div with id="id-edit_grade_btn"
    $(this).addClass('uiSearchItemInvisible');
    $(this).removeClass('uiSearchItemVisible');
});
// ------------------------------------- hide button end -------------------------------------
});
// ------------------------------------- individual function end -------------------------------------

// ------------------------------------- individual function start -------------------------------------
$(document).ready(function() {
  // ------------------------------------- edit button start -------------------------------------
  // Attach a click event handler to the div with id="id-edit_grade_btn"
  $('#id-edit_summary_btn').on('click', function() {
      // Add class 'class_a' to the div with id="id-edit_grade_section"
      $('#id-summary_str_section').addClass('uiSearchItemInvisible');
      $('#id-summary_str_section').removeClass('uiSearchItemVisible');
      $('#id-summary_input_section').addClass('uiSearchItemVisible');
      $('#id-summary_input_section').removeClass('uiSearchItemInvisible');
      $('#id-hide_summary_btn').addClass('uiSearchItemVisible');
      $('#id-hide_summary_btn').removeClass('uiSearchItemInvisible');

      // Remove class 'class_b' from the div with id="id-edit_grade_btn"
      $(this).addClass('uiSearchItemInvisible');
      $(this).removeClass('uiSearchItemVisible');
  });
  // ------------------------------------- edit button end -------------------------------------
  // ------------------------------------- hide button start -------------------------------------
  // Attach a click event handler to the div with id="id-edit_grade_btn"
  $('#id-hide_summary_btn').on('click', function() {
    // Add class 'class_a' to the div with id="id-edit_grade_section"
    $('#id-summary_str_section').addClass('uiSearchItemVisible');
    $('#id-summary_str_section').removeClass('uiSearchItemInvisible');
    $('#id-summary_input_section').addClass('uiSearchItemInvisible');
    $('#id-summary_input_section').removeClass('uiSearchItemVisible');
    $('#id-edit_summary_btn').addClass('uiSearchItemVisible');
    $('#id-edit_summary_btn').removeClass('uiSearchItemInvisible');

    // Remove class 'class_b' from the div with id="id-edit_grade_btn"
    $(this).addClass('uiSearchItemInvisible');
    $(this).removeClass('uiSearchItemVisible');
});
// ------------------------------------- hide button end -------------------------------------
});
// ------------------------------------- individual function end -------------------------------------