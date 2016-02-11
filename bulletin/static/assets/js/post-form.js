/*
    Post Form Javascript
*/
jQuery(document).ready(function() {
    // -------------------------------------------------------------------------
    // Categories dropdowns
    // -------------------------------------------------------------------------
    $('select[name*=categories]').selectize({
        maxItems: 3,
        plugins: ['required-options'],
        required_values: []
    });

    $('select[name*=secondary-categories]').selectize({
        maxItems: 2,
        plugins: ['required-options'],
        required_values: []
    });
});
