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

