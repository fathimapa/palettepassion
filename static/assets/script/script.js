$(document).ready(function () {

    $("#asidebard_btn").click(function () {

        if (!$("#asidenav").hasClass("open_aside")) {
            $("#asidenav").addClass("open_aside");
            $(".content_body").css("margin-left", "0px");
            $(".list_ul_drop>li").addClass("col-xs-6 col-md-3 col-lg-2 col-6");
            $(".content_body").css("display", "block");
        } else {

            $(".list_ul_drop>li").removeClass();
            $("#asidenav").removeClass("open_aside");
            $(".content_body").css("margin-left", "230px");

            if ($(window).width() < 747) {
                $(".content_body").css("display", "flex");
            }
        }

    })



    if ($(window).width() < 747) {


        $("#asidenav").addClass("open_aside");
        $(".content_body").css("margin-left", "0px");
        // $(".content_body").css("display", "flex");
        $(".list_ul_drop>li").addClass("col-xs-6 col-md-3 col-lg-2 col-6");
    }


    $(".listnav>li>a").mouseenter(function () {
        var classs = $(this).find("i").attr("class");

        $(this).find("i").css("padding-left", "3px");
        $(this).find("i").css("margin-right", "5px");

        if (!$(this).hasClass("activepage")) {
            $(this).addClass("activepage");
        }


    })

    $(".listnav>li>a").mouseleave(function () {
        if ($(this).attr("rel") != "active") {
            $(this).removeClass("activepage");
        } else {
            $(this).find("a").css("padding-left", "3px");
            $(this).find("a").css("margin-right", "5px");
        }

        $(this).find("i").css("padding-left", "8px");
        $(this).find("i").css("margin-right", "10px");
    })

    $(".listnav>li>a").click(function () {

        var dropdown = $(this).attr("data-show");
        $(".submenus").slideUp(450);

        $(this).attr("rel", "");
        $(this).removeClass("rel", "activepage");

        var avaible_active = $(".activepage").length;

        $(".activepage").each(function () {
            $(this).removeClass("activepage");
            $(this).attr("rel", "");
        })

        if ($("#" + dropdown).css("display") == "block") {
            $("#" + dropdown).hide(450);
        } else {
            $("#" + dropdown).slideToggle(450);

        }

        $(this).addClass("activepage");
        $(this).attr("rel", "active");
    })

    $(".hide_seekerlist_drop").click(function () {
        var item_control = $(this).attr("data-widget");
        $("#" + item_control).slideToggle()
    })

    $(".remove_seekerlist_drop").click(function () {
        var item_control = $(this).attr("data-widget");
        $("#" + item_control).remove()
    })

    if ($("#asidenav").hasClass("open_aside")) {
        $(".content_body").css("display", "block");
    }

    $("#checkall").click(function () {
        $(".check_select").prop("checked", function (i, oldVal) {

            return !oldVal;
        });
    })


    $(".hide_seekerlist_drop").click(function () {
        var item_control = $(this).attr("data-widget");
        $("#" + item_control).slideToggle()
    })

    $(".remove_seekerlist_drop").click(function () {
        var item_control = $(this).attr("data-widget");
        $("#" + item_control).remove()
    })


    $("#close_activetopaid").click(function () {
        $(".active_to_paid_wrapper").hide();
    })

    $("#activetopaidbtn").click(function () {
        $(".active_to_paid_wrapper").show();
    })




})


function actionData(type, form, input) {

    if (confirm("Are you sure want to execute this function")) {
        $("#" + input).val(type);
        $("#" + form).submit();

    }
}


function checkAll(ele) {
    var checkingElement = $('input[name="check_all"]');

    if (ele.checked) {
        for (var i = 0; i < checkingElement.length; i++) {
            if (checkingElement[i].type == 'checkbox') {
                checkingElement[i].checked = true;
            }
        }
    } else {
        for (var i = 0; i < checkingElement.length; i++) {
            console.log(i)
            if (checkingElement[i].type == 'checkbox') {
                checkingElement[i].checked = false;
            }
        }
    }
}
setTimeout(function(){
	$('#message').fadeOut('slow')
},4000)

  
function showSelectImage(fromid) {
    if ($(window).width() < 522) {
        $("#cmsImagepop").css("display", "block");
    } else {
        $("#cmsImagepop").css("display", "flex");
    }

    $(".upload_imga_center").css("display", "flex");
    $("#fromIdInput").val(fromid);
}




function changetabimage() {
    $("#upload_image_tab").addClass("removeitemtab"); //remove class from tab for hide evcery tab
    $("#showimagedata").removeClass("removeitemtab"); // show clicked tab only here


    if ($("#showimagedata").hasClass("hideimagetab"))  //if clicked tab has hideimagetab
    {
        $("#showimagedata").removeClass("hideimagetab");  // remove hideimagetab class
    }

    $(".upload_media_tab_btn").removeClass("active_media_tab"); //remove tab button border for everywhere
    $(".mediatabbtn").addClass("active_media_tab"); // add button border for selected only
}

$(document).ready(function () {
    $(".tab_file_upload").click(function () {
        var showitem = $(this).attr("data-widget"); // getting button widget

        $(".tab_image_uipload_common").addClass("removeitemtab"); //remove class from tab for hide evcery tab
        $("#" + showitem).removeClass("removeitemtab"); // show clicked tab only here


        if ($("#" + showitem).hasClass("hideimagetab"))  //if clicked tab has hideimagetab
        {
            $("#" + showitem).removeClass("hideimagetab");  // remove hideimagetab class
        }


        $(".tab_file_upload").removeClass("active_media_tab"); //remove tab button border for everywhere
        $(this).addClass("active_media_tab"); // add button border for selected only

    })

    // $(document).on('click', '#deleteImagePopup', function () {
    //     var value_image = $("#setValue").val();

    //     $.ajax({
    //         url: "api/deleteImage.php",                      //Server api to receive the file
    //         type: "POST",
    //         data: { image_name: value_image },
    //         success: function (datas) {
    //             if (datas == 0) {
    //                 alert("Error")
    //             } else if (datas == 1) {
    //                 $(".image_uploaded_list_item.selectedimage").remove();
    //             }

    //         }
    //     });
    // })

    // function getLastUploaded() {
    //     $.ajax(
    //         {
    //             url: "api/getLastUploaded.php",
    //             type: "POST",
    //             success: function (data) {
    //                 $("#uploadImagesList").append(data);
    //             }

    //         }
    //     )
    // }

    // function callPopupimages() {
    //     $.ajax(
    //         {
    //             url: "api/getUploadedImages.php",
    //             type: "POST",
    //             success: function (data) {

    //                 $("#uploadImagesList").append(data);
    //             }

    //         }
    //     )
    // }
    // callPopupimages()


    let row = 0;
    $(document).on('click', '.image_uploaded_list_item', function () {

        if ($(this).hasClass("selectedimage")) {
            $(this).removeClass("selectedimage");
            $(this).find(".selected_image_bg").remove();
        } else {
            const row = $(this).data("row");
            $(this).append('<span class="selected_image_bg" id="removeSelectedImgA' + row + '"></span>');
            $(this).addClass('selectedimage');
        }

        const anySelected = $(".image_uploaded_list_item.selectedimage").length > 0;
        $("#deleteImagePopup, #doneageSelect, #infoImagePopup, #viewImage").prop('disabled', !anySelected);

        let selectedImages = [];
        let selectedId = [];
        $(".image_uploaded_list_item.selectedimage").each(function () {
            selectedImages.push($(this).attr("data-imagename"));
            selectedId.push($(this).attr("data-image-id"));
        });


        $("#idValue").val(selectedId.join(","));
        $("#setValue").val(selectedImages.join(","));

    })
    // $("#infoImagePopup").click(function () {
    //     var selected_images = $(".image_uploaded_list_item.selectedimage").attr("data-imagename");
    //     $.ajax({
    //         url: "api/getImageData.php",                      //Server api to receive the file
    //         type: "POST",
    //         data: { image_name: selected_images },
    //         success: function (datas) {
    //             if (datas == 0) {
    //                 alert("Error")
    //             } else {
    //                 alert(datas);
    //             }

    //         }
    //     });
    // });


    $("#viewImage").click(function () {
        var selected_images = $(".image_uploaded_list_item.selectedimage").attr("data-imagename");

        var fullpath = "web/images/" + selected_images;

        $("#setPopUpImage").attr('src', fullpath);
        $(".imagepopup_view").css("display", "flex");
    })

    $("#close_popup").click(function () {
        $(".imagepopup_view").hide()
    })



    $("#doneageSelect").click(function () {
        var from_id = $("#fromIdInput").val();
        var value_image = $("#setValue").val();

        $("#" + from_id).val(value_image);
        $("#cmsImagepop").hide();
    })

    $("#select_file").click(function () {
        $("#imagFile").click();
    })



    // $("#getBigSize").click(function () {
    //     var type = $("#getBigSize").attr("data-type");
    //     $.ajax({
    //         url: "api/getBigImage.php",
    //         type: "POST",
    //         data: { type: type },
    //         success: function (data) {
    //             $(".imageuploadlist>ul>div").remove();
    //             $("#uploadImagesList").append(data);
    //             if ($("#getBigSize").attr("data-type") == "big") {
    //                 $("#getBigSize").text("GET SMALLER SIZE FILES");
    //                 $("#getBigSize").attr("data-type", "smaller");
    //             } else {
    //                 $("#getBigSize").text("GET BIG SIZE FILE ONLY");
    //                 $("#getBigSize").attr("data-type", "big");
    //             }


    //         }
    //     });
    // })

    // function uploadfile() {

    //     var file_data = $('.fileToUpload').prop('files')[0];    //Fetch the file
    //     var form_data = new FormData();
    //     form_data.append("file", file_data);


    //     $.ajax({
    //         url: "api/imageUploadTab.php",                      //Server api to receive the file
    //         type: "POST",
    //         dataType: 'script',
    //         cache: false,
    //         contentType: false,
    //         processData: false,
    //         data: form_data,
    //         success: function (dat2) {
    //             if (dat2 == 0) {
    //                 alert("Unable to Upload")
    //             } else if (dat2 == 1) {
    //                 getLastUploaded();
    //                 changetabimage();
    //             }

    //         }
    //     });
    // }



    $("#close_modal_popup_image").click(function () {
        $("#cmsImagepop").hide();
    })



})