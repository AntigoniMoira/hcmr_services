import Ajax from './Ajax.js';
import Utils from './Utils.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());
const utils = new Utils();

const ActivateUser = function () {

    $('.activate-users-modal').on('show.bs.modal', function (e) {
        utils.hidemsg('#activate-fail-message');
        utils.hidemsg('#delete-fail-message');
        const $trigger = $(e.relatedTarget);
        const email = $trigger.val();
        var data = {
            email : email,
            reason: $('#delete-reason').val()
        };
    
        $(this).find('.modal-title').text($trigger.val());
        $(".btn-delete").off().on('click', function () {
            data['reason']=$('#delete-reason').val();
            ajax.post(HomeRoutes.home.delete_user, data).then((return_data) => {
                if (return_data.success === true) {
                    $($trigger).closest('tr').remove();
                    $(".modal .close").click()
                }else{
                    utils.showmsg('#delete-fail-message',return_data.message);
                }
            }).catch((error) => {
                const err = new AjaxError(error);
                utils.showmsg('#delete-fail-message',err.msg);
            });
        });

        $(".btn-activate").off().on('click', function () {
            ajax.post(HomeRoutes.home.activate_user, data).then((return_data) => {
                if (return_data.success === true) {
                    /*$($trigger).closest('tr').remove();
                    $(".modal .close").click()*/
                    window.location.href = HomeRoutes.home.activate_user;
                }else{
                    utils.showmsg('#activate-fail-message',return_data.message);
                }
            }).catch((error) => {
                const err = new AjaxError(error);
                utils.showmsg('#activate-fail-message',err.msg);
            });
        });
        
    });
}

export {ActivateUser};
