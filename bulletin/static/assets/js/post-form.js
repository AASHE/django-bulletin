/*
    Post Form Javascript
*/
jQuery(document).ready(function() {
    // -------------------------------------------------------------------------
    // Categories dropdowns
    // -------------------------------------------------------------------------
    $('#id_categories').selectize({
        maxItems: 3
    });

    $('#id_secondary_categories').selectize({
        maxItems: 2
    });

    $('#id_primary_category').selectize({
        maxItems: 1
    });

    // Remove 'form-control' so widget displays in the correct position:
    $('.selectize-control').removeClass('form-control');

    // Remove 'form-control' so dropdown is opaque:
    $('.selectize-dropdown').removeClass('form-control');
});
