/*
 Use auto-formatting for any variables with datatype: ssn
*/

$(document).on('daPageLoad', function(){
inputs = $("input[type='ssn']");

for (var i=0; i<inputs.length; i++) {
      inputs[i].onkeyup = function() {
      var val = this.value.replace(/\D/g, '');
      var newVal = '';

      if(val.length > 4) {
        this.value = val;
      }

      if((val.length > 3) && (val.length < 6)) {
        newVal += val.substr(0, 3) + '-';
        val = val.substr(3);
      }

      if (val.length > 5) {
        newVal += val.substr(0, 3) + '-';
        newVal += val.substr(3, 2) + '-';
        val = val.substr(5);
      }
      newVal += val;
      this.value = newVal.substring(0, 11);
      };    
  }
});