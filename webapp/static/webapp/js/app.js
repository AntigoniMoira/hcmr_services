import {loginViaAuthServer} from "./oauth-via-authserver.js";
import {logoutViaAuthServer} from "./oauth-via-authserver.js";
import {mapsFunction} from "./map.js";
import {poseidonDB} from "./poseidon_db.js"
import {ActivateUser} from "./activate-user.js";
import {EditUserProfile} from "./user-profile.js";


$( "#login-btn" ).click(loginViaAuthServer);
$( "#logout-btn" ).click(logoutViaAuthServer);

$(document).ready(function() {
    mapsFunction();
    poseidonDB();
    ActivateUser();
    EditUserProfile();
});