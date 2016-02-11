/*
    Post Form Javascript
*/
jQuery(document).ready(function() {
    // -------------------------------------------------------------------------
    // Categories dropdowns
    // -------------------------------------------------------------------------
    $('select[name*=categories]').selectize({
        maxItems: 3
    });

    $('select[name*=secondary-categories]').selectize({
        maxItems: 2
    });

    $('.selectize-control').removeClass('form-control');

    $('.selectize-dropdown').removeClass('form-control');
});
