$(document).ready(function () {


    $('.product_size_var').on('change', function () {
        var selectedSize = $(this).val().trim();
        var productId = $(this).attr("data-product-id");

         let url='/store/get_price_by_size/'+productId+'/'+selectedSize

        

        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log(data)
                $('#product-price').text('$' + data.price);
            },
            error: function (xhr, errmsg, err) {
                console.log(err);
            }
        });
    });
});
 