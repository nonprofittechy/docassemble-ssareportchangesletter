$(document).on('daPageLoad', function(){
    var maxID = 1;
    
    // test

    function getTemplateRow() {
        var x = document.getElementById("templateRow").cloneNode(true);
        x.id = "";
        x.style.display = "";
        var inputs = x.getElementsByTagName('input');

        for (var i = 0; i<inputs.length; i++) {
            inputs.item(i).id = incrementInBtoa(inputs.item(i).id, maxID)
            inputs.item(i).name = incrementInBtoa(inputs.item(i).name, maxID)
            if (inputs.item(i).hasAttribute('aria-describedby') ) {
                aria = inputs.item(i).getAttribute('aria-describedby');
                inputs.item(i).setAttribute('aria-describedby', 'addon-' + incrementInBtoa(aria.replace('addon-',''), maxID));
            }
        } 

        var labels = x.getElementsByTagName('label');
        for (var i=0;i<labels.length;i++){
            labels.item(i).setAttribute('for', incrementInBtoa(labels.item(i).getAttribute('for'),maxID));
        }

        var divs = x.getElementsByTagName('div');
        for (var i=0; i<divs.length; i++) {
            var id = divs.item(i).id;
            if (id.includes('addon-') ) {
                id.replace('addon-','');
                divs.item(i).id = 'addon-' + incrementInBtoa(id,maxID);
            }
        }

        ++maxID;

        return x;
    }
 
    function incrementInBtoa(text,newInc) {
        try {
            return btoa(atob(text).replace(/\[0\]/,'[' + newInc + ']'));
        } catch(err) {
            return text
        }
    }

    function addRow() {
        var t = document.getElementById("theTable");
        var rows = t.getElementsByTagName("tr");
        var r = rows[rows.length - 1];
        r.parentNode.insertBefore(getTemplateRow(), r);

    }
    $("#add_row").click(function(e){e.preventDefault(); addRow(); return false;})
});