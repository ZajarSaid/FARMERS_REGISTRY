


$(document).ready(function() {
    $('#regionSelect').change(function() {
        var regionId = $(this).val();
        var url = $(this).data('url');  // Get the URL from the data attribute

        $.ajax({
            url: url,
            data: {
                'region_id': regionId
            },
            success: function(data) {
                $('#districtSelect').empty();
                $.each(data, function(index, district) {
                    $('#districtSelect').append($('<option>', {
                        value: district.id,
                        text: district.name
                    }));
                });
            }
        });
    });
});
