/*
Add onChange="functionName(id) in input to validate
*/

/* Change input style if invalid */
function warning(textfield){
	textfield.style.borderColor = 'red';
    return;
}



/* Check if required input is empty, ideally on sumbission and orChange */
function isEmpty(textfield){
    var pattern = /^\s*$/;
    if (!pattern.test(textfield)){
        warning(textfield);
    }
    return;
}



/* Check if input is a valid Canadian postal code */
function isValidPostalCode(postalcode) { 
    var pattern = /^\s*[ABCEGHJKLMNPRSTVXYabceghjklmnprstvxy]{1}\d{1}[a-zA-Z]{1}\s{0,1}\d{1}[a-zA-Z]{1}\d{1}\s*$/;
    if ( isEmpty(postalcode) || !pattern.test(postalcode) ){
    	warning(postalcode);
    }
    return;
} 

/* Check if input is a valid zip code */
function isValidZipCode(zipcode) { 
    var pattern = /^\s*\d{5}(-\d{4})?\s*$/;
    if ( isEmpty(zipcode) || !pattern.test(zipcode) ){
    	warning(zipcode);
    }
    return;
} 

/* Check if input is a valid either Canadian postal code or zip code */
function isValidPostalAndZipCode(postalcode) {
	var pattern = /(^\s*\d{5}(-\d{4})?\s*$)|(^\s*[ABCEGHJKLMNPRSTVXYabceghjklmnprstvxy]{1}\d{1}[a-zA-Z]{1}\s{0,1}\d{1}[a-zA-Z]{1}\d{1}\s*$)/;
    if ( isEmpty(postalcode) || !pattern.test(postalcode) ){
    	warning(postalcode);
    }
    return;
}

/* Check if a password meets requirement */
function isValidPassword() {

}

/* Check if two passwords match */
function passwordsMatch() {
    var password1 = $("#password1").value;
    var password2 = $("#password2").value;

    if( isEmpty(password2) || password1 != password2) {
        warning(password2);
    }
    return;
}

/* Check if input is a valid email address. Meets RFC2822 grammar. */
function isValidEmailAddress(emailAddress) {
    var pattern = /^([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x22([^\x0d\x22\x5c\x80-\xff]|\x5c[\x00-\x7f])*\x22)(\x2e([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x22([^\x0d\x22\x5c\x80-\xff]|\x5c[\x00-\x7f])*\x22))*\x40([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x5b([^\x0d\x5b-\x5d\x80-\xff]|\x5c[\x00-\x7f])*\x5d)(\x2e([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x5b([^\x0d\x5b-\x5d\x80-\xff]|\x5c[\x00-\x7f])*\x5d))*$/;
    if ( isEmpty(emailAddress) || !pattern.test(emailAddress) ){
        warning(emailAddress);
    }
    return;
}

