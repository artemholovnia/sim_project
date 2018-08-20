function get_template(url, selector, callback) {
    $.get(url, function (data) {
        template = jQuery("<div>").append( jQuery.parseHTML(data) ).find(selector);
        callback(template);
    })
}