import Ajax from './Ajax.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());

var sessionvar

const apiRequest = function () {

sessionvar= sessionStorage.getItem('access_token');

ajax.getAT('http://localhost:8000/api/platforms/',sessionvar, {}).then((return_data) => {
        console.log(return_data);
    }).catch((error) => {
      const err = new AjaxError(error);
      console.log(err.msg);
    });

}; //function END
export {apiRequest};