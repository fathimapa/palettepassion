// === QTY JS === //
function wcqib_refresh_quantity_increments() {
	jQuery("div.quantity:not(.buttons_added), td.quantity:not(.buttons_added)").each(function (a, b) {
		var c = jQuery(b);
		c.addClass("buttons_added"), c.children().first().before('<input type="button" value="-" class="minus" />'), c.children().last().after('<input type="button" value="+" class="plus" />')
	})
}
// String.prototype.getDecimals || (String.prototype.getDecimals = function () {
// 	var a = this,
// 		b = ("" + a).match(/(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/);
// 	return b ? Math.max(0, (b[1] ? b[1].length : 0) - (b[2] ? +b[2] : 0)) : 0
// }), jQuery(document).ready(function () {
// 	wcqib_refresh_quantity_increments()
// }), jQuery(document).on("updated_wc_div", function () {
// 	wcqib_refresh_quantity_increments()
// }), jQuery(document).on("click", ".plus, .minus", function () {
// 	var a = jQuery(this).closest(".quantity").find(".qty"),
// 		b = parseFloat(a.val()),
// 		c = parseFloat(a.attr("max")),
// 		d = parseFloat(a.attr("min")),
// 		e = a.attr("step");
// 	b && "" !== b && "NaN" !== b || (b = 0), "" !== c && "NaN" !== c || (c = ""), "" !== d && "NaN" !== d || (d = 0), "any" !== e && "" !== e && void 0 !== e && "NaN" !== parseFloat(e) || (e = 1), jQuery(this).is(".plus") ? c && b >= c ? a.val(c) : a.val((b + parseFloat(e)).toFixed(e.getDecimals())) : d && b <= d ? a.val(d) : b > 0 && a.val((b - parseFloat(e)).toFixed(e.getDecimals())), a.trigger("change")
// });

// wishlist script //
$(document).ready(function () {
	$('.like-icon, .like-button').on('click', function (e) {
		e.preventDefault();
		$(this).toggleClass('liked');
		$(this).children('.like-icon').toggleClass('liked');
	});
});

// menu script //
$(document).ready(function () {
	var fixHeight = function () {
		$(".navbar-nav").css(
			"max-height",
			document.documentElement.clientHeight - 8000
		);
	};

	fixHeight();

	$(window).resize(function () {
		fixHeight();
	});

	$(".navbar .navbar-toggler").on("click", function () {
		fixHeight();
	});

	$(".navbar-toggler, .overlay").on("click", function () {
		$(".mobileMenu, .overlay").toggleClass("open");
		console.log("clicked");
	});
});


// === Dropdown === //

$('.ui.dropdown')
	.dropdown()
	;

// === Model === //
$('.ui.modal')
	.modal({
		blurring: true
	})
	.modal('show')
	;

// === Tab === //
$('.menu .item')
	.tab()
	;

// === checkbox Toggle === //
$('.ui.checkbox')
	.checkbox()
	;

// === Toggle === //
$('.enable.button')
	.on('click', function () {
		$(this)
			.nextAll('.checkbox')
			.checkbox('enable')
			;
	})
	;


// Payment Method Accordion //
$('input[name="paymentmethod"]').on('click', function () {
	var $value = $(this).attr('value');
	$('.return-departure-dts').slideUp();
	$('[data-method="' + $value + '"]').slideDown();
});



//  Countdown //
$(".product_countdown-timer").each(function () {
	var $this = $(this);
	$this.countdown($this.data('countdown'), function (event) {
		$(this).text(
			event.strftime('%D days %H:%M:%S')
		);
	});
});



function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// === Banner Home === //
$('.offers-banner').owlCarousel({
	loop: true,
	margin: 30,
	nav: false,
	dots: false,
	autoplay: true,
	autoplayTimeout: 3000,
	autoplayHoverPause: true,
	responsive: {
		0: {
			items: 1
		},
		600: {
			items: 2
		},
		1000: {
			items: 2
		},
		1200: {
			items: 3
		},
		1400: {
			items: 3
		}
	}
})

// Category Slider
$('.cate-slider').owlCarousel({
	loop: true,
	margin: 30,
	nav: true,
	dots: false,
	navText: ["<i class='uil uil-angle-left'></i>", "<i class='uil uil-angle-right'></i>"],
	responsive: {
		0: {
			items: 2
		},
		600: {
			items: 2
		},
		1000: {
			items: 4
		},
		1200: {
			items: 6
		},
		1400: {
			items: 6
		}
	}
})

// Featured Slider
$('.featured-slider').owlCarousel({
	items: 8,
	loop: false,
	margin: 10,
	nav: true,
	dots: false,
	navText: ["<i class='uil uil-angle-left'></i>", "<i class='uil uil-angle-right'></i>"],
	responsive: {
		0: {
			items: 1
		},
		600: {
			items: 2
		},
		1000: {
			items: 3
		},
		1200: {
			items: 4
		},
		1400: {
			items: 5
		}
	}
})

// === Date Slider === //
$('.date-slider').owlCarousel({
	loop: false,
	margin: 10,
	nav: false,
	dots: false,
	responsive: {
		0: {
			items: 3
		},
		600: {
			items: 4
		},
		1000: {
			items: 5
		},
		1200: {
			items: 6
		},
		1400: {
			items: 7
		}
	}
})

// === Banner Home === //
$('.life-slider').owlCarousel({
	loop: true,
	margin: 30,
	nav: true,
	dots: false,
	autoplay: true,
	autoplayTimeout: 3000,
	autoplayHoverPause: true,
	navText: ["<i class='uil uil-angle-left'></i>", "<i class='uil uil-angle-right'></i>"],
	responsive: {
		0: {
			items: 1
		},
		600: {
			items: 2
		},
		1000: {
			items: 2
		},
		1200: {
			items: 3
		},
		1400: {
			items: 3
		}
	}
})

// === Testimonials Slider === //
$('.testimonial-slider').owlCarousel({
	loop: true,
	margin: 30,
	nav: true,
	dots: false,
	autoplay: true,
	autoplayTimeout: 3000,
	autoplayHoverPause: true,
	navText: ["<i class='uil uil-angle-left'></i>", "<i class='uil uil-angle-right'></i>"],
	responsive: {
		0: {
			items: 1
		},
		600: {
			items: 2
		},
		1000: {
			items: 2
		},
		1200: {
			items: 3
		},
		1400: {
			items: 3
		}
	}
})

// Category Slider
$('.team-slider').owlCarousel({
	loop: true,
	margin: 30,
	nav: false,
	dots: false,
	responsive: {
		0: {
			items: 1
		},
		600: {
			items: 2
		},
		1000: {
			items: 3
		},
		1200: {
			items: 4
		},
		1400: {
			items: 4
		}
	}
})


setTimeout(function () {
	$('#message').fadeOut('slow')
}, 4000)


$(document).ready(function () {
	$('.wishlist-button').click(function () {
		var productId = $(this).data('product-id');
		var wishlistAction = $(this).data('action');  // Get the intended action

		$.ajax({
			url: '/cart/wishlist/',  // Adjust this URL if needed
			type: wishlistAction === 'add' ? 'POST' : 'DELETE',  // Set request type based on action
			data: {
				product_id: productId,
				csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
			},
			success: function (response) {
				if (response.success) {
					if (wishlistAction === 'add') {
						// Update button/icon for added state
						$(this).text('Added to Wishlist');
						$(this).removeClass('add-to-wishlist').addClass('added-to-wishlist');
					} else {
						// Update button/icon for removed state
						$(this).text('Add to Wishlist');
						$(this).removeClass('added-to-wishlist').addClass('add-to-wishlist');
					}
					// Optionally display success or removal message
				} else {
					// Handle errors
				}
			}
		});
	});
});


//add to wishlist

$(".wishlistButton").click(addToWhishlist);

function addToWhishlist(e) {

	

	let variant= $(this).attr("data-product-id");



	var url = '/cart/whishlist/add/'

	var data = {
		variant: variant,
	};

	$.ajax({
		type: "POST",
		url: url,  // Replace with the actual URL for your view
		dataType: "json",
		data: JSON.stringify(data),
		headers: {
			"X-Requested-With": "XMLHttpRequest",
			"X-CSRFToken": getCookie("csrftoken"),
		},
		success: (data) => {
			if (data.status === "success") {
				// success
				console.log(data);
				
				// location.reload()

			} else {
				// Password change error
				console.log(data);
				window.location.href = data.login_url;
				// Display the error message on the page
			}

		},
		error: (xhr, status, error) => {
			// Display the error message on the page
			console.log("error");
			console.log(error);
		}
	});


}