class Utils {
    constructor() {}

    allowOnlyNumbers(event) {
        if (isNaN(parseInt(event.key)) && event.key !== '+'  && event.key !== '-' && event.key !== ' ' && event.key !== '.' && event.key !== ',' && event.key !== '(' && event.key !== ')' 
            && event.key !== 'Backspace' && event.key !== 'Delete' && event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') {
            event.preventDefault();
        }
    }

    allowCertainLength(event, Curlen, AllLen) {
        if (Curlen === AllLen) {
            event.preventDefault();
        }
    }

    validate_email(email) {
        if (
            /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
                email
            )
        ) {
            return true;
        } else {
            return false;
        }
    }

    showmsg(id, error_message) {
        $(id).html("*" + error_message + "");
        $(id).show();
    }
  
    hidemsg(id) {
            $(id).html("");
            $(id).hide();
    }

    getUrlParameter(sParam) {
        var sPageURL = window.location.search.substring(1),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;
    
        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');
    
            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
            }
        }
    };
}
export default Utils