function countCharsAnswers(obj){var maxLength = 100;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("charNumAnswers").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  }else{
    document.getElementById("charNumAnswers").innerHTML = '<span style="color: var(--company-greyed-out-color);">'+strLength+' out of '+maxLength+' characters';
  }
}