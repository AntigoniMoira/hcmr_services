import {loginValidation} from "./login-validation.js";
import {loginViaAPI} from "./login-via-api.js";
import {logoutViaAPI} from "./login-via-api.js";
import {atToSessionStorage} from "./login-via-api.js";
import {apiRequest} from "./api-requests.js";
import {mapsFunction} from "./map.js";


$( "#login-btn" ).click(loginViaAPI);
$( "#logout-btn" ).click(logoutViaAPI);
$( "#api-btn" ).click(apiRequest);
$("#authorizationForm > div > div > input.btn.btn-large.btn-primary").click(function() {
    console.log(alert("hello from accept"));
});

$(document).ready(function() {
    atToSessionStorage();
    loginValidation();
    mapsFunction();
    
});