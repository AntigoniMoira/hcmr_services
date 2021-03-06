import Ajax from './Ajax.js';
import Utils from './Utils.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());
const utils = new Utils();


// Steppers
const poseidonDB = function () {

    $('#date-from').datetimepicker({
        format: 'DD/MM/YYYY',
        pickTime: false
    });
    $('#date-to').datetimepicker({
        format: 'DD/MM/YYYY',
        pickTime: false
    });

    $("#date-from").on("dp.change", function (e) {
        $('#date-to').data("DateTimePicker").setMinDate(e.date);
    });
    $("#date-to").on("dp.change", function (e) {
        $('#date-from').data("DateTimePicker").setMaxDate(e.date);
    });

    //Initialize tooltips
    $('.nav-tabs > li a[title]').tooltip();

    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        var $target = $(e.target);
        if ($target.parent().hasClass('disabled')) {
            return false;
        }
    });

    $(".next-step").click(function (e) {
        var step = $(this).val();
        var $active = $('.wizard .nav-tabs li.active');
        content(step);
        $active.next().removeClass('disabled');
        $active.addClass('disabled');
        nextTab($active);
    });

    $(".prev-step").click(function (e) {
        var step = $(this).val();
        clear_content(step);
        var $active = $('.wizard .nav-tabs li.active');
        $active.prev().removeClass('disabled');
        $active.addClass('disabled');
        prevTab($active);
    });

    $('#platforms').multiselect({
        nonSelectedText: 'Select Platform(s)',
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        includeSelectAllOption: true,
        buttonWidth: '400px'
    });
};

function nextTab(elem) {
    $(elem).next().find('a[data-toggle="tab"]').click();
}

function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}

function content(step) {
    var date_from = $('#date-from-input').val().split('/');
    var date_to = $('#date-to-input').val().split('/');

    //step1 -> step2 / TimeFrame -> Platform(s)
    if (step === 'date') {
        var date_data = {
            start_date: date_from[2] + '-' + date_from[1],
            end_date: date_to[2] + '-' + date_to[1]
        };

        ajax.get(HomeRoutes.home.platforms_between, date_data).then((return_data) => {
            if (return_data['data'].length == 0) {
                utils.showmsg('#select-platforms-fail-message', 'Data not available.');
            }
            else{
                utils.hidemsg('#select-platforms-fail-message');
                for (var x = 0; x < return_data['data'].length; x++) {
                    var plat_name = return_data['data'][x].platform;
                    $('#platforms').append("<option value=" + plat_name + ">" + plat_name + "</option>");
                }
            }
            $("#platforms").multiselect('rebuild');
        }).catch((error) => {
            const err = new AjaxError(error);
            console.log(err);
        });
    }
    //step2 -> step3 / Platforms -> Parameter(s)
    if (step === 'params') {
        $("#platforms option:selected").each(function () {
            var str = $(this).text();
            var params_data = {
                platform: str,
                start_date: date_from[2] + '-' + date_from[1],
                end_date: date_to[2] + '-' + date_to[1]
            };

            $('#param-selects').append('<div class=row><select id=' + str + ' name=parameters[] multiple class=form-control collapse></select></div>');
            $('#' + str).multiselect({
                nonSelectedText: str,
                enableFiltering: true,
                enableCaseInsensitiveFiltering: true,
                includeSelectAllOption: true,
                maxHeight: 200,
                buttonWidth: '100%',
                buttonText: function(options, select) {
                    return select.attr('id') +' ('+ options.length +')';
                },
            });

            ajax.get(HomeRoutes.home.measurements_between, params_data).then((return_data) => {
                var param_list = return_data['data'][0].param.split('#');
                if (str.startsWith("T")) {
                    for (var x = 0; x < param_list.length; x++) {
                        var param = param_list[x].split('^');
                        var param_pressure = param[1] + '^' + param[0].split('@')[1];
                        $('#' + str).append('<option value=' + param_pressure + '>' + param[0].replace(/@/g, "") + '</option>');
                    }
                } else {
                    for (var x = 0; x < param_list.length; x++) {
                        var param = param_list[x].split('^');
                        $('#' + str).append('<option value=' + param[1] + '>' + param[0].replace(/@/g, "") + '</option>');
                    }
                }
                $('#' + str).multiselect('rebuild');
            }).catch((error) => {
                const err = new AjaxError(error);
                console.log(err);
            });
        });
    }

    if (step === 'complete') {
        $('#inform-user').hide();
        $('#sum-date-from').html('<strong>Date from: </strong>' + $('#date-from-input').val());
        $('#sum-date-to').html('<strong>Date to: </strong>' + $('#date-to-input').val());
        var count_platforms = 1;
        var tbody = '';
        $("#platforms option:selected").each(function () {
            var str = $(this).text();
            //console.log(str);
            var platforms_params='';
            //var abbr='';
            //var depths='';
            if (str.startsWith("T")) {
                var prev_param='';
                $('#' + str + ' option:selected').each(function () {
                    var param_pres = $(this).val().split('^');
                    //console.log('param_pres[0]:' + param_pres[0]);
                    //console.log('param_pres[1]:' + param_pres[1]);
                    if(prev_param==param_pres[0]){
                        platforms_params = platforms_params + param_pres[1] + ', ';
                    }
                    else{
                        //tbody=tbody + '<tr> <th scope="row">'+ count_platforms +'</th><td>'+ str +'</td><td>'+ platforms_params +'</td><td>'+ abbr +'</td><td>'+ depths +'</td></tr>'
                        //depths = depths + '<br>' + param_pres[1];
                        platforms_params = platforms_params + '<br>' + $(this).html() + ',';
                    }
                    prev_param=param_pres[0];
                });
            }
            else{
                $('#' + str + ' option:selected').each(function () {
                    platforms_params = platforms_params + $(this).html() + ',<br>';
                });
            }
            tbody=tbody + '<tr> <th scope="row">'+ count_platforms +'</th><td>'+ str +'</td><td>'+ platforms_params +'</td></tr>'
            count_platforms = count_platforms + 1;
        });
        $("#sum-table tbody").html(tbody);
    }

    //Final step. Data collection and send to backend
    if (step === 'submit') {
        var ts_list = [];
        var pr_list = [];
        var count_ts = 0;
        var count_pr = 0;
        $("#platforms option:selected").each(function () {
            var str = $(this).text();
            if (str.startsWith("T")) {
                ts_list.push({
                    plat: str,
                    params: {}
                });
                $('#' + str + ' option:selected').each(function () {
                    var param_pres = $(this).val().split('^');
                    if (typeof (ts_list[count_ts].params[param_pres[0]]) === "undefined") {
                        ts_list[count_ts].params[param_pres[0]] = [param_pres[1]];
                    } else {
                        ts_list[count_ts].params[param_pres[0]].push(param_pres[1]);
                    }
                });
                count_ts = count_ts + 1;
            } else {
                pr_list.push({
                    plat: str,
                    params: []
                });
                $('#' + str + ' option:selected').each(function () {
                    pr_list[count_pr].params.push($(this).val());
                });
                count_pr = count_pr + 1;
            }
        });
        var submit_data = {
            data: JSON.stringify({
                user_email: $('#email').val(),
                dt_of_request: Date.now(),
                dt_from: $('#date-from-input').val(),
                dt_to: $('#date-to-input').val(),
                platforms: {
                    'TS': ts_list,
                    'PR': pr_list
                }
            })
        }
        /*ajax.post(HomeRoutes.home.create_netcdf, submit_data).then((return_data) => {
            if (return_data.success==true){
                document.getElementById("overlay").style.display = "block";
            }
        }).catch((error) => {
            const err = new AjaxError(error);
            console.log(err);
        });*/
        var request = $.ajax({
            url: HomeRoutes.home.create_netcdf,
            type: 'POST',
            dataType: 'json',
            data: submit_data,
            contentType: 'application/json',
            beforeSend: (xhr) => {
                      xhr.setRequestHeader('X-CSRFToken', ajax._getCookie('csrftoken'));
                      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                  }
          });
          document.getElementById("overlay").style.display = "block";
    }

}

$('#overlay').click(function (e) {
    document.getElementById("overlay").style.display = "none";
    location.reload();
  });

function clear_content(step) {

    //step2 ->step1 / Platform(s) -> TimeFrame 
    if (step === 'date') {
        $('#platforms').find('option').remove();
    }

    //step3 -> step2 / Parameter(s) -> Platform(s)
    if (step === 'params') {
        $('#param-selects').empty();
    }
}

export {
    poseidonDB
};