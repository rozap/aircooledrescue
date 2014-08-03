// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



/* define a new sync method, alias the old one (ew) */
var os = Backbone.sync;
Backbone.sync = function(method, model, options) {
    var opts = options || {};
    /* only need a token for non-get requests */
    if (method == 'create' || method == 'update' || method == 'delete') {
        // CSRF token value is in an embedded meta tag 
        var csrfToken = getCookie('csrftoken');

        opts.beforeSend = function(xhr){
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        };
    }

    /* proxy the call to the old sync method */
    return os(method, model, opts);
};
