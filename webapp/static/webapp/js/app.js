import {loginValidation} from "./login-validation.js";
import {loginViaAPI} from "./oauth-via-api.js";
import {logoutViaAPI} from "./oauth-via-api.js";
import {atToSessionStorage} from "./oauth-via-api.js";
import {apiRequest} from "./api-requests.js";
import {mapsFunction} from "./map.js";


$( "#login-btn" ).click(loginViaAPI);
$( "#logout-btn" ).click(logoutViaAPI);
$( "#api-btn" ).click(apiRequest);

$(document).ready(function() {
    atToSessionStorage();
    loginValidation();
    mapsFunction();
    
});