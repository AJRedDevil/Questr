/*
Add onChange="functionName(id) in input to validate
*/

/* Change input style if invalid */
function warning(textfield){
	textfield.style.borderColor = 'red';
}

/* Check if input is a valid Canadian postal code */
function validatePostalCodeCanada(postalcode) { 
    var pattern = /^\s*[ABCEGHJKLMNPRSTVXYabceghjklmnprstvxy]{1}\d{1}[a-zA-Z]{1}\s{0,1}\d{1}[a-zA-Z]{1}\d{1}\s*$/;
    if (!pattern.test(postalcode)){
    	warning(postalcode);
    }
} 

/* Check if input is a valid zip code */
function validateZipCodeUSA(zipcode) { 
    var pattern = /^\s*\d{5}(-\d{4})?\s*$/;
    if (!pattern.test(zipcode)){
    	warning(zipcode);
    }
} 

/* Check if input is a valid either Canadian postal code or zip code */
function validatePostalAndZipCode(postalcode) {
	var pattern = /(^\s*\d{5}(-\d{4})?\s*$)|(^\s*[ABCEGHJKLMNPRSTVXYabceghjklmnprstvxy]{1}\d{1}[a-zA-Z]{1}\s{0,1}\d{1}[a-zA-Z]{1}\d{1}\s*$)/;
    if (!pattern.test(postalcode)){
    	warning(postalcode);
    }
}

/* Check if two passwords match */
function validatePasswords() {
    var password1 = $("#password1").value;
    var password2 = $("#password2").value;

    if(password1 != password2) {
        warning(password2);
    }
    
}

/* Check if input is a valid email address. Meets RFC2822 grammar. */
function validateEmailAddress(emailAddress) {
    var pattern = /^([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x22([^\x0d\x22\x5c\x80-\xff]|\x5c[\x00-\x7f])*\x22)(\x2e([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x22([^\x0d\x22\x5c\x80-\xff]|\x5c[\x00-\x7f])*\x22))*\x40([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x5b([^\x0d\x5b-\x5d\x80-\xff]|\x5c[\x00-\x7f])*\x5d)(\x2e([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x5b([^\x0d\x5b-\x5d\x80-\xff]|\x5c[\x00-\x7f])*\x5d))*$/;
    if (!pattern.test(postalcode)){
        warning(postalcode);
    }
}