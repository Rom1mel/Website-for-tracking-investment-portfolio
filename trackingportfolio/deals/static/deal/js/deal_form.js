$(document).ready(function () {
    const assetSelect = $('#id_asset');
    const searchUrl = assetSelect.data('search-url');

    assetSelect.select2({
        ajax: {
            url: searchUrl,
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term || '',
                    type: $('#asset-type-filter').val()
                };
            },
            processResults: function (data) {
                return {
                    results: data.results
                };
            }
        },
        minimumInputLength: 1,
        placeholder: 'Введите название или тикер актива'
    });

    $('#asset-type-filter').on('change', function () {
        assetSelect.val(null).trigger('change');
    });
});