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