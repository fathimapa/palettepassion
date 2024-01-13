var mobilenumberError =document.getElementById('mobilenumber-error');
var emailError =document.getElementById('email-error');
var submitError =document.getElementById('submit-error');
function validateAddAddressMobilenumber(){
	var mobilenumber = document.getElementById('id_phone').value;
	if(mobilenumber.length==0){
		mobilenumberError.innerHTML = 'mobile no required';
		return false;
	}
	if(mobilenumber.length !==10){
		mobilenumberError.innerHTML = 'mobile no should 10 digits';
		return false;
	}
	if(!mobilenumber.match(/^[0-9]{10}$/)){
		mobilenumberError.innerHTML = 'only digits please';
		return false;
	}
	mobilenumberError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
	return true;

}
function validateAddAddressEmail(){
	var email = document.getElementById('id_email').value;
	if(email.length==0){
		emailError.innerHTML = 'email required';
		return false;
	}
	if(!email.match(/^[A-Za-z\._\-[0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/)){
		emailError.innerHTML = 'email invalid'
		return false;
	}
	emailError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
	return true;

}
function validateAddAddresForm(){
	if(!validateAddAddressMobilenumber() || !validateAddAddressEmail()){
		submitError.style.display = 'block';
		submitError.innerHTML = 'please correct form';
		setTimeout(function(){submitError.style.display = 'none';},3000);
		return false;
	}
	return true;
}