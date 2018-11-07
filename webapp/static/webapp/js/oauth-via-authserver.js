import Ajax from './Ajax.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());

const loginViaAuthServer = function () {
    const url=HomeRoutes.auth.login + '?response_type=code&state=random_state_string&client_id=NwVaE1ddbUDyzlCf0MvdVy7fRbwGCskjXtMPJy0z&URI=' + HomeRoutes.home.access_token;
    window.location.href=url;
    
}; //function END

const registerViaAuthServer = function () {
    window.location.href=HomeRoutes.auth.register;
    
}; //function END

const logoutViaAuthServer = function () {
        ajax.get(HomeRoutes.home.logout, {}).then((return_data) => {
            console.log(return_data.success);
            if (return_data.success === true) {
                window.location.href = return_data.redirectUri;
            } 
            else if (return_data.success === false) {
                window.location.href=HomeRoutes.home.error
            }
        }).catch((error) => {
            const err = new AjaxError(error);
            console.log(err.msg);
        });  
}; //function END


export {loginViaAuthServer, registerViaAuthServer, logoutViaAuthServer};