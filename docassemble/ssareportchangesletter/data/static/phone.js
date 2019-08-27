/*
 Use auto-formatting for any variables with datatype: tel
*/

$(document).on('daPageLoad', function(){
    $("input[type='tel']").keyup(function() {
      var curchr = this.value.length;
      var curval = $(this).val();
      if (curchr == 3) {
          $(this).val("(" + curval + ")" + "-");
      } else if (curchr == 9) {
          $(this).val(curval + "-");
      }
    });
  });