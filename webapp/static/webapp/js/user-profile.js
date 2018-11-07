import Ajax from './Ajax.js';
import Utils from './Utils.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());
const utils = new Utils();

const EditUserProfile = function () {

     //Phone validation
     $('#editPhone').keypress(function (e) {
        utils.allowOnlyNumbers(e);
        //utils.allowCertainLength(e, $(this).val().length, 10);
    });

    $(".form-profile-edit").submit(function (e) {
        e.preventDefault();
        $('#edit-profile').modal('toggle');
        utils.hidemsg('#profile-success-message');
        utils.hidemsg('#profile-fail-message');
        const user_data = {
            data: JSON.stringify({
                username: $("#editUserName").val(),
                firstname: $("#editFirstName").val(),
                lastname: $("#editLastName").val(),
                bday: $("#editDBirthday").val(),
                gender: $("#editGender").val(),
                country: $("#editCountry").val(),
                institution: $("#editInstitution").val(),
                phone: $("#editPhone").val(),
                email: $("#profile_email").html(),
                description: $("#editDescription").val()
            })
        };
        ajax.post(HomeRoutes.home.user_profile, user_data).then((return_data) => {
            if (return_data.success === true) {
                window.location.href = HomeRoutes.home.user_profile;
            } else {
                utils.showmsg('#profile-fail-message', return_data.message);
            }
        }).catch((error) => {
            const err = new AjaxError(error);
            utils.showmsg('#profile-fail-message', err.msg);
        });
    });

    $(".form-change-password").submit(function (e) {
        e.preventDefault();
        utils.hidemsg('#change-psw-fail-message1');
        utils.hidemsg('#change-psw-fail-message2');
        utils.hidemsg('#profile-success-message');
        const data = {
                email: $("#profile_email").html(),
                old_psw: $("#old-password").val(),
                new_psw: $("#new-password").val(),
                conf_new_psw: $("#confirm-new-password").val()
            };
        if (data.new_psw !== data.conf_new_psw){
            utils.showmsg("#change-psw-fail-message2", "New Passwords must match!");
        }
        else if (data.new_psw.length < 6) {
            utils.showmsg("#change-psw-fail-message2", "New Password must be more than 5 characters.");
        }
        else{
            ajax.post(HomeRoutes.home.change_password, data).then((return_data) => {
                if (return_data.success === true) {
                    $('#change-password').modal('toggle');
                    utils.showmsg('#profile-success-message', return_data.message);
                } else {
                    utils.showmsg('#change-psw-fail-message1', return_data.message);
                }
            }).catch((error) => {
                const err = new AjaxError(error);
                utils.showmsg('#change-psw-fail-message2', err.msg);
            });
        }
    });
}
export {
    EditUserProfile
};