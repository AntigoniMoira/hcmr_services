import Ajax from './Ajax.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());

const loginViaAPI = function () {
    const url='http://localhost:8000/o/authorize/?response_type=code&state=random_state_string&client_id=a4KPlQ7SV2qjsSMF6TOKWvmZ36QEUI25E8Dvn6sL&URI=http://localhost:9000/webapp/access_token/';

    ajax.get(url, {}).then((return_data) => {
        
    }).catch((error) => {
        const err = new AjaxError(error);
        console.log(err.msg);
    });
    
}; //function END

var sessionvar

var data={
    'token': sessionStorage.getItem('access_token'),
    'token_type_hint': 'access_token',
    'client_id': 'a4KPlQ7SV2qjsSMF6TOKWvmZ36QEUI25E8Dvn6sL',
    'client_secret': 'heRhnOayEOLyh0cWR2C8RqPhrAhOR8Cmrgx4a5eMmht7sFY6bQcRIphsT9TUkL62yMjdJXL6t9sXn0ynxLGSrH0hPr1r1dKqOahncNJHcvRV2W4uTqnMZwzY61LPj8tI'
}

const logoutViaAPI = function () {
        ajax.post('http://localhost:8000/o/revoke_token/', data).then((return_data) => {
            console.log(return_data);
        /*}).catch((error) => {
            const err = new AjaxError(error);
            console.log(err.msg);*/
        });
    
}; //function END

const atToSessionStorage = function () {
    sessionStorage.clear();
    ajax.get('http://localhost:9000/webapp/get_session/?key=access_token', {}).then((return_data) => {
        sessionvar= return_data.data;
        sessionStorage.setItem('access_token', sessionvar);
    }).catch((error) => {
      const err = new AjaxError(error);
      console.log(err.msg);
    });
    ajax.get('http://localhost:9000/webapp/get_session/?key=refresh_token', {}).then((return_data) => {
        sessionvar= return_data.data;
        sessionStorage.setItem('refresh_token', sessionvar);
    }).catch((error) => {
      const err = new AjaxError(error);
      console.log(err.msg);
    });
}; //function END

export {loginViaAPI, logoutViaAPI, atToSessionStorage};