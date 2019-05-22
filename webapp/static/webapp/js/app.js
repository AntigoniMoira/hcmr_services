import {loginViaAuthServer} from "./oauth-via-authserver.js";
import {registerViaAuthServer} from "./oauth-via-authserver.js";
import {logoutViaAuthServer} from "./oauth-via-authserver.js";
import {poseidonDB} from "./poseidon_db.js"
import {ActivateUser} from "./activate-user.js";
import {EditUserProfile} from "./user-profile.js";
import { WeatherForecast } from "./weather_forecast.js";


//$( "#login-btn" ).click(loginViaAuthServer);
//$( "#register-btn" ).click(registerViaAuthServer);
$( "#login-link" ).click(loginViaAuthServer);
$( "#register-link" ).click(registerViaAuthServer);
$( "#logout-btn" ).click(logoutViaAuthServer);


$(document).ready(function() {
    /*$(window).on("hashchange", function(e){
        $('#loader').show();
    });
    $(window).on("load", function (e) {
        $('#loader').hide();
    });*/
    //document.getElementById("overlay").style.display = "block";
    if($.trim($('.alert').html())==''){
        $(".alert").hide();
    }
    poseidonDB();
    ActivateUser();
    EditUserProfile();
    WeatherForecast();
});