var password1Error =document.getElementById('password1-error');
var password2Error =document.getElementById('password2-error');
var password3Error =document.getElementById('password3-error');
var submitError =document.getElementById('submit-error');
function validateChangePassword1(){
	var password1 = document.getElementById('password1').value;
	if(password1.length==0){
	    password1Error.innerHTML = 'password required'
	    return false;
	}
	if(password1.length !==6){
		password1Error.innerHTML = 'should 6 characters ';
		return false;
	}
	if(!password1.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/)){
		password1Error.innerHTML = 'Atleat one character and one number'
		return false;
	   
	} 
	password1Error.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
	return true;
}
function validateChangePassword2(){
	var password2 = document.getElementById('password2').value;
	if(password2.length==0){
	    password2Error.innerHTML = 'password required'
	    return false;
	}
	if(password2.length !==6){
		password2Error.innerHTML = 'password should 6 characters';
		return false;
	}
	if(!password2.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/)){
		password2Error.innerHTML = 'Atleat one character and one number'
		return false;
	} 
	password2Error.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
		return true;
}
function validateChangePassword3(){
    console.log('loooooooooo')
	var password3 = document.getElementById('password3').value;
	if(password3.length==0){
	    password3Error.innerHTML = 'password required'
	    return false;
	}
	if(password3.length !==6){
		password3Error.innerHTML = 'password should 6 characters';
		return false;
	}
	if(!password3.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/)){
		password3Error.innerHTML = 'Atleat one character and one number'
		return false;
	} 
	password3Error.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
		return true;
}
function validateFormProfileChange(){
	if(!validateChangePassword1() || !validateChangePassword1()||!validateChangePassword3()){
		submitError.style.display = 'block';
		submitError.innerHTML = 'please correct form';
		setTimeout(function(){submitError.style.display = 'none';},3000);
		return false;
	}
	return true;
}