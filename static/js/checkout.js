$(document).ready(function () {


    function paymentSuccess(razorpay_payment_id, razorpay_order_id, razorpay_signature,product_order_id) {
        var token = $('input[name="csrfmiddlewaretoken"]').val(); 


        var form = document.createElement('form');
        form.action = "/order/razorpay_payment_success/";
        form.method = "POST";

        // Create hidden input fields for the data
        var paymentIdInput = document.createElement('input');
        paymentIdInput.type = 'hidden';
        paymentIdInput.name = 'razorpay_payment_id';
        paymentIdInput.value = razorpay_payment_id;
        form.appendChild(paymentIdInput);

        var paymentIdInput = document.createElement('input');
        paymentIdInput.type = 'hidden';
        paymentIdInput.name = 'csrfmiddlewaretoken';
        paymentIdInput.value = token;
        form.appendChild(paymentIdInput);

        console.log(token)

        var orderIdInput = document.createElement('input');
        orderIdInput.type = 'hidden';
        orderIdInput.name = 'razorpay_order_id';
        orderIdInput.value = razorpay_order_id;
        form.appendChild(orderIdInput);

        var signatureInput = document.createElement('input');
        signatureInput.type = 'hidden';
        signatureInput.name = 'razorpay_signature';
        signatureInput.value = razorpay_signature;
        form.appendChild(signatureInput);

        var csrfTokenInput = document.createElement('input');
        csrfTokenInput.type = 'hidden';
        csrfTokenInput.name = 'csrfmiddlewaretoken';
        csrfTokenInput.value = $('input[name="csrfmiddlewaretoken"]').val();
        form.appendChild(csrfTokenInput);

        
        var orderIDInput = document.createElement('input');
        orderIDInput.type = 'hidden';
        orderIDInput.name = 'order_id';  // Set the desired name for the input field
        orderIDInput.value = product_order_id;
        form.appendChild(orderIDInput);
        console.log(product_order_id);

	    


       
        document.body.appendChild(form);
        form.submit();
 
        document.body.removeChild(form);
    }
    $('.payWithrazorpay').click(function (e) {
         var token = $('input[name="csrfmiddlewaretoken"]').val(); 
         var product_order_id = $(this).attr('data-order-id');
         console.log(product_order_id)

         

    
        $.ajax({
            url: "/store/create_razorpay_order/",
            method: "POST",
            data: { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11", 'csrfmiddlewaretoken': token },
            success: (response) => {
                console.log(response?.order?.id)
                var options = {
                    "key": "rzp_test_v1Zu1znDq4Sk12", // Enter the Key ID generated from the Dashboard
                    "amount": "50000", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "Acme Corp",
                    "description": "Test Transaction",
                    "image": "https://example.com/your_logo",
                    "order_id": response?.order?.id, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                    "handler": function (response) {
                        paymentSuccess(response.razorpay_payment_id, response.razorpay_order_id, response.razorpay_signature, response.product_order_id)
                    },
                
                    "prefill": {
                        "name": "Gaurav Kumar",
                        "email": "gaurav.kumar@example.com",
                        "contact": "9000090000"
                    },
                    "notes": {
                        "address": "Razorpay Corporate Office"
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };


                var rzp1 = new Razorpay(options);

                rzp1.open();
            }
        })



    });


});